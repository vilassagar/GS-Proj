from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from app.models.gr_yojana import Yojana, GR
from app.services.dal.dto.gr_yojana_dto import YojanaDTO, GRDTO

class YojanaDal:
    @staticmethod
    def create_yojana(db: Session, name: str, created_by: int) -> Yojana:
        new_yojana = Yojana(name=name, created_by=created_by)
        db.add(new_yojana)
        db.commit()
        db.refresh(new_yojana)
        return new_yojana

    @staticmethod
    def get_all_yojanas(db: Session) -> List[YojanaDTO]:
        yojanas = db.query(Yojana).filter(Yojana.is_active).all()
        return [YojanaDTO.to_dto(y) for y in yojanas]

    @staticmethod
    def get_yojana_by_id(db: Session, yojana_id: int) -> YojanaDTO:
        yojana = db.query(Yojana).filter(Yojana.is_active, Yojana.id == yojana_id).first()
        return YojanaDTO.to_dto(yojana)


class GRDal:
    @staticmethod
    def create_gr(db: Session, gr_data: dict) -> GR:
        new_gr = GR(**gr_data)
        db.add(new_gr)
        db.commit()
        db.refresh(new_gr)
        return new_gr

    @staticmethod
    def get_gr_by_number(db: Session, gr_number: str) -> Optional[GRDTO]:
        gr = db.query(GR).filter(GR.gr_number == gr_number, GR.is_active).first()
        return GRDTO.to_dto(gr) if gr else None

    @staticmethod
    def get_grs_by_date_range(db: Session, start_date: date, end_date: date) -> List[GRDTO]:
        grs = db.query(GR).filter(
            GR.effective_date.between(start_date, end_date),
            GR.is_active
        ).all()
        return [GRDTO.to_dto(gr) for gr in grs]