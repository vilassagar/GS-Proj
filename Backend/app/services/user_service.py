from sqlalchemy.orm import Session
from typing import List
from app.services.dal.user_dal import UserDal

class UserService:
    @staticmethod
    def get_users_by_block_id(block_id: int, db: Session) -> List:
        return UserDal.get_users_block_id(db, block_id)

    @staticmethod
    def get_users_by_district_id(district_id: int, db: Session) -> List:
        return UserDal.get_users_by_district(db, district_id)