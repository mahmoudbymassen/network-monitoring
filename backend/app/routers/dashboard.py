from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from collections import defaultdict
from datetime import datetime, timedelta

from ..core.database import get_db
from ..models.appareil import Appareil
from ..models.alerte import Alerte

router = APIRouter()

@router.get("/")
async def get_dashboard(db: Session = Depends(get_db)):
    """Professional Dashboard - Summary for Management"""
    
    # Get all devices
    appareils = db.query(Appareil).all()
    
    total = len(appareils)
    en_ligne = len([a for a in appareils if a.statut == "en_ligne"])
    hors_ligne = total - en_ligne
    pourcentage = round((en_ligne / total * 100), 2) if total > 0 else 0

    # Stats by floor
    par_etage = defaultdict(int)
    for a in appareils:
        par_etage[str(a.etage)] += 1

    # Stats by type
    par_type = defaultdict(int)
    for a in appareils:
        par_type[a.type_appareil.value] += 1

    # Recent alerts (last 24 hours)
    recent_alerts = db.query(Alerte)\
                      .filter(Alerte.date_creation >= datetime.utcnow() - timedelta(days=1))\
                      .order_by(Alerte.date_creation.desc())\
                      .limit(5)\
                      .all()

    last_alert = None
    if recent_alerts:
        last_alert = {
            "message": recent_alerts[0].message,
            "type": recent_alerts[0].type_alerte.value,
            "date": recent_alerts[0].date_creation
        }

    return {
        "status": "success",
        "dashboard": {
            "total_appareils": total,
            "en_ligne": en_ligne,
            "hors_ligne": hors_ligne,
            "pourcentage_en_ligne": pourcentage,
            "par_etage": dict(par_etage),
            "par_type": dict(par_type),
            "recent_alerts_count": len(recent_alerts),
            "last_alert": last_alert,
            "last_updated": datetime.utcnow()
        }
    }