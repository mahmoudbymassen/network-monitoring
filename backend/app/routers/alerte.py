from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..core.database import get_db
from ..models.alerte import Alerte, TypeAlerte, Severite

router = APIRouter()

@router.get("/", response_model=List[dict])
def get_all_alertes(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 50,
    acknowledged: bool = None
):
    """Get all alerts"""
    query = db.query(Alerte)
    
    if acknowledged is not None:
        query = query.filter(Alerte.accusee == acknowledged)
    
    alertes = query.order_by(Alerte.date_creation.desc()).offset(skip).limit(limit).all()
    
    return [
        {
            "id": a.id,
            "appareil_id": a.appareil_id,
            "type_alerte": a.type_alerte,
            "severite": a.severite,
            "message": a.message,
            "date_creation": a.date_creation,
            "accusee": a.accusee
        } for a in alertes
    ]

@router.get("/unread")
def get_unread_alertes(db: Session = Depends(get_db)):
    """Get only unread (unacknowledged) alerts"""
    alertes = db.query(Alerte)\
                .filter(Alerte.accusee == False)\
                .order_by(Alerte.date_creation.desc())\
                .all()
    
    return [
        {
            "id": a.id,
            "type_alerte": a.type_alerte.value,
            "severite": a.severite.value,
            "message": a.message,
            "date_creation": a.date_creation
        } for a in alertes
    ]

@router.put("/{alerte_id}/acknowledge")
def acknowledge_alert(alerte_id: int, db: Session = Depends(get_db)):
    """Mark an alert as read"""
    alerte = db.query(Alerte).filter(Alerte.id == alerte_id).first()
    if not alerte:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    alerte.accusee = True
    db.commit()
    
    return {"message": "Alert acknowledged", "alerte_id": alerte_id}