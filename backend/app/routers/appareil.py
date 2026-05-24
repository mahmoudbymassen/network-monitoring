from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..core.database import get_db
from ..models.appareil import Appareil
from ..schemas.appareil import AppareilCreate, AppareilResponse

router = APIRouter()

@router.get("/", response_model=List[AppareilResponse])
def get_all_appareils(db: Session = Depends(get_db)):
    appareils = db.query(Appareil).all()
    return appareils

@router.get("/{appareil_id}", response_model=AppareilResponse)
def get_appareil(appareil_id: int, db: Session = Depends(get_db)):
    appareil = db.query(Appareil).filter(Appareil.id == appareil_id).first()
    if not appareil:
        raise HTTPException(status_code=404, detail="Appareil not found")
    return appareil

@router.post("/", response_model=AppareilResponse)
def create_appareil(appareil: AppareilCreate, db: Session = Depends(get_db)):
    db_appareil = Appareil(**appareil.dict())
    db.add(db_appareil)
    db.commit()
    db.refresh(db_appareil)
    return db_appareil