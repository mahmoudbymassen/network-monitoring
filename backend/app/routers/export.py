from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import StreamingResponse
import pandas as pd
from io import BytesIO
from datetime import datetime

from ..core.database import get_db
from ..models.appareil import Appareil

router = APIRouter()

@router.get("/devices/excel")
def export_devices_to_excel(db: Session = Depends(get_db)):
    """Export all devices to Excel file"""
    
    appareils = db.query(Appareil).all()
    
    data = []
    for a in appareils:
        data.append({
            "ID": a.id,
            "Adresse IP": a.adresse_ip,
            "Adresse MAC": a.adresse_mac,
            "Nom d'Hôte": a.nom_hote,
            "Marque": a.marque,
            "Type d'Appareil": a.type_appareil.value,
            "Étage": a.etage,
            "Sous-Réseau": a.sous_reseau,
            "Statut": a.statut.value,
            "Latence (ms)": a.latence_ms,
            "Premier Détection": a.premier_detection,
            "Dernière Détection": a.derniere_detection
        })
    
    df = pd.DataFrame(data)
    
    # Create Excel file in memory
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Appareils_Réseau')
    
    output.seek(0)
    
    filename = f"Appareils_Réseau_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx"
    
    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": f"attachment; filename={filename}"
        }
    )


@router.get("/devices/csv")
def export_devices_to_csv(db: Session = Depends(get_db)):
    """Export devices to CSV"""
    appareils = db.query(Appareil).all()
    
    data = [{
        "ip": a.adresse_ip,
        "mac": a.adresse_mac,
        "hostname": a.nom_hote,
        "marque": a.marque,
        "type": a.type_appareil.value,
        "floor": a.etage,
        "status": a.statut.value,
        "latency_ms": a.latence_ms
    } for a in appareils]
    
    df = pd.DataFrame(data)
    output = BytesIO()
    df.to_csv(output, index=False, encoding='utf-8')
    output.seek(0)
    
    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=appareils_reseau.csv"}
    )