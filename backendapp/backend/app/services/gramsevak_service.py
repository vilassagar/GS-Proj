import base64
import logging
from datetime import datetime
from typing import List, Optional, Dict, Any

from botocore.exceptions import ClientError
from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session

import boto3

from app.config import settings
from app.core.core_exceptions import NotFoundException, InvalidRequestException
from app.models.enums.approval_status import ApprovalStatus, ApprovalStatusRequest
from app.schemas.gramsevak_schema import GramsevakListItem, GramsevakDetailResponse
from app.services.dal.document_dal import UserDocumentDal
from app.services.dal.role_dal import RoleDal
from app.services.dal.user_dal import UserDal
from app.services.dal.user_hierarchy_dal import DistrictDal, BlockDal, GramPanchayatDal


# Configure S3 client with credentials from settings
s3_client = boto3.client(
    "s3",
    aws_access_key_id=settings.aws_access_key_id,
    aws_secret_access_key=settings.aws_secret_access_key,
    region_name=settings.aws_default_region
)
bucket_name = settings.aws_s3_bucket



class GramsevakService:

    @staticmethod
    def read_document_content(s3_key: str) -> Optional[str]:
        """
        Read document content from S3 and return it as a Base64-encoded string.
        """
        try:
            # Fetch the file from S3
            response = s3_client.get_object(Bucket=bucket_name, Key=s3_key)
            file_content = response['Body'].read()

            # Encode the file content to Base64
            return base64.b64encode(file_content).decode("utf-8")

        except ClientError as e:
            logging.error(f"Error reading file from S3 {s3_key}: {str(e)}")
            return None
        except Exception as e:
            logging.error(f"Unexpected error reading file from S3 {s3_key}: {str(e)}")
            return None

    @staticmethod
    def get_gramsevak_list(
            db: Session,
            search_term: Optional[str] = None,
            status_filter: ApprovalStatusRequest = ApprovalStatusRequest.ALL
    ) -> List[GramsevakListItem]:

        print("In service layer")

        gramsevak_role = RoleDal.get_role_by_name(db, "gramSevak")
        if not gramsevak_role:
            raise NotFoundException("Gram Sevak role not found")

        print("Here 1")

        users = UserDal.get_gramsevaks(
            db,
            role_id=gramsevak_role.id,
            search_term=search_term,
            status_filter=status_filter
        )

        print("Here 2")

        result = []
        for user in users:
            district = DistrictDal.get_district_by_id(db, user.district_id) if user.district_id is not None else None
            block = BlockDal.get_block_by_id(db, user.block_id) if user.block_id is not None else None
            gramPanchayat=GramPanchayatDal.get_gram_panchayat_by_id(db,user.gram_panchayat_id) if user.gram_panchayat_id is not None else None
            result.append({
                "id": user.id,
                "firstName": user.first_name,
                "lastName": user.last_name,
                "email": user.email,
                "gramPanchayat":gramPanchayat.gram_panchayat_name, 
                "block": block.block_name if block else "N/A",
                "district": district.district_name if district else "N/A",
                "serviceId": 'temp_service_id',
                "isApproved": user.status == ApprovalStatus.APPROVED,
                "documentsUploaded": user.documents_uploaded
            })

        print("Here 3")

        return result[::-1]

    @staticmethod
    def get_gramsevak_details(db: Session, gramsevak_id: int) -> GramsevakDetailResponse:
        user = UserDal.get_user_with_details_by_id(db, gramsevak_id)

        if not user or not user.role_id:
            raise InvalidRequestException("User Role not found")

        gramsevak_role = RoleDal.get_role_by_name(db=db, name="gramSevak")
        if not gramsevak_role or gramsevak_role.id != user.role_id:
            raise InvalidRequestException("User is not assigned as Gram Sevak")

        district = DistrictDal.get_district_by_id(db=db, district_id=user.district_id) if user.district_id is not None else None
        block = BlockDal.get_block_by_id(db=db, block_id=user.block_id) if user.block_id is not None else None
        gram_panchayat = GramPanchayatDal.get_gram_panchayat_by_id(db=db, gp_id=user.gram_panchayat_id) if user.gram_panchayat_id is not None else None

        documents = UserDocumentDal.get_user_documents(db, user.id)

        user_data = user.to_camel()

        user_data['documents'] = [
            {
                "documentTypeId": doc.document_type_id,
                "documentType": doc.document_type,
                "document": GramsevakService.read_document_content(doc.file_path),  # Now reads from S3
                "verification_status": doc.verification_status
            } for doc in documents
        ]

        return GramsevakDetailResponse(**user_data)

    @staticmethod
    def update_gramsevak_status(
            db: Session,
            gramsevak_id: int,
            new_status: ApprovalStatus
    ):

        print("Hitting The Service layer:")
        user = UserDal.get_user_by_id(db, gramsevak_id)

        if not user or not user.role_id:
            raise NotFoundException("Gramsevak not found")

        print("Here 2", user.__dict__)

        if RoleDal.get_role_by_name(db=db, name="gramSevak").id != user.role_id:
            raise NotFoundException("Role id not found")

        print("Calling DAL")

        print("Here 3 Calling Update status DAL")

        UserDal.update_user(
            db,
            user_id=gramsevak_id,
            update_dict={"status": new_status}
        )

        return {"message": "Status updated successfully"}

    @staticmethod
    async def upload_gs_docs(
        db: Session, 
        gramsevak_id: int, 
        documents: Dict[int, UploadFile],
        metadata: Dict[int, Dict[str, Any]] = None
    ) -> dict:
        """
        Upload documents with their associated metadata
        
        Args:
            db: Database session
            gramsevak_id: User ID
            documents: Dict mapping document_type_id to file
            metadata: Dict mapping document_type_id to field values
        """
        user = UserDal.get_user_by_id(db, gramsevak_id)
        if not user:
            raise NotFoundException("Requesting User not Found")

        uploaded_docs = []
        metadata = metadata or {}
        
        for doc_id, file in documents.items():
            try:
                # Save the file
                file_path = await GramsevakService.save_file_to_storage(
                    file=file, user_id=gramsevak_id, document_type_id=doc_id
                )

                # Create the document record
                user_doc = UserDocumentDal.create_user_document(
                    db=db,
                    user_id=gramsevak_id,
                    document_type_id=doc_id,
                    file_path=file_path
                )
                
                # If there's metadata for this document, update the field_values
                if doc_id in metadata and metadata[doc_id]:
                    # Update the document with field values
                    UserDocumentDal.update_user_document(
                        db=db,
                        document_id=user_doc.id,
                        update_data={
                            'field_values': metadata[doc_id]
                        }
                    )
                
                uploaded_docs.append(user_doc)

            except Exception as e:
                print(f"Error uploading document {doc_id}: {str(e)}")
                raise HTTPException(
                    status_code=400,
                    detail=f"Failed to upload document {file.filename}: {str(e)}"
                )

        UserDal.set_documents_uploaded_to_true(db=db, user_id=gramsevak_id)

        # Check and handle mandatory documents logic
        MANDATORY_DOC_IDS = [15, 10, 11,19,20,24,9]  # Example: replace with your actual mandatory doc IDs

        def are_all_mandatory_docs_uploaded(db, user_id):
            from app.models.documents import UserDocument
            uploaded_doc_ids = set(
                doc.document_type_id
                for doc in db.query(UserDocument)
                .filter_by(user_id=user_id)
                .all()
            )
            return all(doc_id in uploaded_doc_ids for doc_id in MANDATORY_DOC_IDS)

        # After uploading all documents
        if are_all_mandatory_docs_uploaded(db, gramsevak_id):
            # Mark DocumentUploadComplete (set a flag or status in DB)
            user = db.query(User).filter_by(id=gramsevak_id).first()
            user.document_upload_complete = True
            db.commit()

        return {
            "message": "Documents uploaded successfully",
            "uploaded_count": len(uploaded_docs)
        }
    
    @staticmethod
    async def save_file_to_storage(file: UploadFile, user_id: int, document_type_id: int) -> str:
        """
        Save file to S3 and return the S3 key.
        """
        try:
            # Generate S3 path like: user_docs/user_<id>/doc_type_<id>/filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            new_filename = f"{timestamp}_{file.filename}"
            s3_key = f"user_docs/user_{user_id}/doc_type_{document_type_id}/{new_filename}"

            # Read file content
            file_content = await file.read()

            # Upload to S3
            s3_client.put_object(
                Bucket=bucket_name,
                Key=s3_key,
                Body=file_content
            )

            # Return the S3 key (relative path)
            return s3_key

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to upload file to S3: {str(e)}"
            )