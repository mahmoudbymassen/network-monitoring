from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from ..core.database import get_db
from ..models.appareil import Appareil
from ..models.alerte import Alerte

router = APIRouter()

@router.get("/summary")
async def get_full_report(db: Session = Depends(get_db)):
    """Complete Summary Report - Perfect for Supervisor"""
    
    appareils = db.query(Appareil).all()
    alertes = db.query(Alerte).order_by(Alerte.date_creation.desc()).limit(10).all()

    # Statistics
    total = len(appareils)
    online = len([a for a in appareils if a.statut.value == "en_ligne"])
    offline = total - online

    # By Type
    by_type = {}
    for a in appareils:
        t = a.type_appareil.value
        by_type[t] = by_type.get(t, 0) + 1

    # By Floor
    by_floor = {}
    for a in appareils:
        f = a.etage
        by_floor[f] = by_floor.get(f, 0) + 1

    return {
        "status": "success",
        "report": {
            "generated_at": datetime.utcnow().isoformat(),
            "network_summary": {
                "total_devices": total,
                "online_devices": online,
                "offline_devices": offline,
                "online_percentage": round((online / total * 100), 2) if total > 0 else 0
            },
            "devices_by_type": by_type,
            "devices_by_floor": by_floor,
            "recent_alerts": [
                {
                    "id": a.id,
                    "type": a.type_alerte.value,
                    "severity": a.severite.value,
                    "message": a.message,
                    "date": a.date_creation
                } for a in alertes
            ],
            "health_status": "Good" if offline <= 2 else "Warning" if offline <= 5 else "Critical"
        }
    }