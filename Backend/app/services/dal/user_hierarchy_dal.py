from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.users_hierarchy import District, Block, GramPanchayat
from app.services.dal.dto.user_hierarchy_dto import DistrictDTO, BlockDTO, GramPanchayatDTO


class DistrictDal:
    @staticmethod
    def get_district_by_id(db: Session, district_id: int) -> Optional[DistrictDTO]:
        district = db.query(District).filter(
            District.id == district_id,
            District.is_active
        ).first()
        return DistrictDTO.to_dto(district) if district else None

    @staticmethod
    def get_all_districts(db: Session) -> List[DistrictDTO]:
        districts = db.query(District).filter(District.is_active).all()
        return [DistrictDTO.to_dto(d) for d in districts]


class BlockDal:
    @staticmethod
    def get_block_by_id(db: Session, block_id: int) -> Optional[BlockDTO]:
        block = db.query(Block).filter(
            Block.id == block_id,
            Block.is_active
        ).first()
        return BlockDTO.to_dto(block) if block else None

    @staticmethod
    def get_blocks_by_district(db: Session, district_id: int) -> List[BlockDTO]:
        blocks = db.query(Block).filter(
            Block.district_id == district_id,
            Block.is_active
        ).all()
        return [BlockDTO.to_dto(b) for b in blocks]

    @staticmethod
    def get_blocks_by_search_term(db: Session, search_term: str) -> List[BlockDTO]:

        blocks = db.query(Block).filter(
            Block.name.ilike(f"%{search_term}%"),
            Block.is_active
        ).all()

        return [BlockDTO.to_dto(b) for b in blocks]

    @staticmethod
    def get_all_active_blocks(db: Session) -> List[BlockDTO]:
        blocks = db.query(Block).filter(
            Block.is_active
        ).all()

        return [BlockDTO.to_dto(b) for b in blocks]


class GramPanchayatDal:
    @staticmethod
    def get_gram_panchayat_by_id(db: Session, gp_id: int) -> Optional[GramPanchayatDTO]:
        gp = db.query(GramPanchayat).filter(
            GramPanchayat.id == gp_id,
            GramPanchayat.is_active
        ).first()
        return GramPanchayatDTO.to_dto(gp) if gp else None

    @staticmethod
    def get_gp_by_block(db: Session, block_id: int) -> List[GramPanchayatDTO]:
        gps = db.query(GramPanchayat).filter(
            GramPanchayat.block_id == block_id,
            GramPanchayat.is_active
        ).all()
        return [GramPanchayatDTO.to_dto(gp) for gp in gps]
