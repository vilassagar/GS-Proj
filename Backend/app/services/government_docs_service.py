import os
import uuid
from datetime import datetime
from pathlib import Path
from fastapi import UploadFile, HTTPException, status
from sqlalchemy.orm import Session
import aiofiles
import aioboto3
import boto3

from app.config import settings
from app.schemas.government_docs_schema import BookUploadSchema, GRUploadSchema
from app.services.dal.department_dal import DepartmentDal
from app.services.dal.government_docs_dal import GovernmentDocsDal
from app.services.dal.gr_dal import YojanaDal


s3_client = boto3.client("s3")
bucket_name = settings.aws_s3_bucket


class GovernmentDocsService:

    @staticmethod
    async def upload_book(
            db: Session,
            book_data: BookUploadSchema,
            file: UploadFile
    ) -> dict:
        # Validate department exists
        department = DepartmentDal.get_department_by_id(db, book_data.department_id)
        if not department:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Department not found"
            )

        # Save file
        file_path = await GovernmentDocsService._save_file(
            file=file,
            category="books",
            department_id=book_data.department_id,
            original_name=file.filename
        )

        # Create book record
        book = GovernmentDocsDal.create_book(
            db=db,
            title=book_data.subject,
            department_id=book_data.department_id,
            file_path=file_path,
            created_by=None  # Set to actual user ID if authenticated
        )

        return {
            "message: ": "GR Created successfully"
        }
        # return {
        #     "id": book.id,
        #     "title": book.title,
        #     "filePath": file_path,
        #     "createdAt": book.created_at
        # }

    @staticmethod
    async def upload_gr(
            db: Session,
            gr_data: GRUploadSchema,
            file: UploadFile
    ) -> dict:
        # Validate department exists
        department = DepartmentDal.get_department_by_id(db, gr_data.department_id)
        if not department:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Department not found"
            )

        # Validate Yojana exists
        yojana = YojanaDal.get_yojana_by_id(db, gr_data.yojana_id)
        if not yojana:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Yojana not found"
            )

        # Check for duplicate GR number
        if GovernmentDocsDal.get_gr_by_number(db, gr_data.gr_number):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="GR with this number already exists"
            )

        # Save file
        file_path = await GovernmentDocsService._save_file(
            file=file,
            category="grs",
            department_id=gr_data.department_id,
            original_name=file.filename
        )

        # Create GR record
        gr = GovernmentDocsDal.create_gr(
            db=db,
            gr_number=gr_data.gr_number,
            gr_code=gr_data.gr_code,
            department_id=gr_data.department_id,
            yojana_id=gr_data.yojana_id,
            subject=gr_data.subject,
            effective_date=gr_data.effective_date,
            file_path=file_path,
            created_by=None  # Set to actual user ID if authenticated
        )

        return {
            "message: ": "GR Created successfully"
            # "id": gr.id,
            # "grNumber": gr.gr_number,
            # "filePath": file_path,
            # "effectiveDate": gr.effective_date
        }

    # @staticmethod
    # async def _save_file(file: UploadFile, category: str, department_id: int, original_name: str) -> str:
    #     try:
    #         # Create directory structure
    #         base_dir = Path("static") / "government_docs" / category / f"dept_{department_id}"
    #         base_dir.mkdir(parents=True, exist_ok=True)
    #
    #         # Generate unique filename
    #         timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    #         # file_ext = Path(original_name).suffix
    #         # unique_id = uuid.uuid4().hex[:6]
    #         new_filename = f"{timestamp}_{original_name}"
    #         file_path = base_dir / new_filename
    #
    #         # Save file
    #         async with aiofiles.open(file_path, "wb") as buffer:
    #             content = await file.read()
    #             await buffer.write(content)
    #
    #         return str(file_path.relative_to("static"))
    #
    #     except Exception as e:
    #         raise HTTPException(
    #             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #             detail=f"Failed to save file: {str(e)}"
    #         )

    @staticmethod
    async def _save_file(file: UploadFile, category: str, department_id: int, original_name: str) -> str:
        try:
            # Generate S3 path like: government_docs/<category>/dept_<id>/filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            new_filename = f"{timestamp}_{original_name}"
            s3_key = f"government_docs/{category}/dept_{department_id}/{new_filename}"

            # Read file content
            file_content = await file.read()

            # Upload to S3
            s3_client.put_object(
                Bucket=bucket_name,
                Key=s3_key,
                Body=file_content
            )

            # Return the relative path (without 'static')
            return s3_key

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to upload file to S3: {str(e)}"
            )

    @staticmethod
    async def get_docs(db):
        books = GovernmentDocsDal.get_books(db=db)

        grs = GovernmentDocsDal.get_grs(db=db)

        return {
            "books": books,
            "grs": grs
        }

