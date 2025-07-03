from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.roles import Role
from app.services.dal.dto.roles_dto import RoleDTO

class RoleDal:
    @staticmethod
    def get_role_by_name(db: Session, name: str) -> Optional[RoleDTO]:
        role = db.query(Role).filter(Role.name == name, Role.is_active).first()

        # print("In Role DAL printing role", role.__dict__)
        print("\n printing role DTO: ", RoleDTO.to_dto(role).__dict__ if role else None)
        return RoleDTO.to_dto(role) if role else None

    @staticmethod
    def get_all_roles(db: Session) -> List[RoleDTO]:
        roles = db.query(Role).filter(Role.is_active).all()
        return [RoleDTO.to_dto(role) for role in roles]