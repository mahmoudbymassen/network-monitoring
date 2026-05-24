from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Dict

from ..core.database import get_db
from ..utils.network_scanner import NetworkScanner

router = APIRouter()

@router.post("/start")
async def start_network_scan(
    ip_range: str = Query("192.168.1.0/24", description="IP range to scan"),
    deep_scan: bool = Query(False, description="Enable deep scan with Nmap (slower but more accurate)"),
    db: Session = Depends(get_db)
):
    """Start network discovery scan"""
    try:
        print(f"🚀 Starting scan on {ip_range} | Deep Scan: {deep_scan}")
        
        devices = await NetworkScanner.arp_scan(ip_range)
        
        await NetworkScanner.save_discovered_devices(
            devices,
            db,
            deep_scan_enabled=deep_scan
        )
        
        return {
            "status": "success",
            "message": f"Scan completed on {ip_range}",
            "devices_found": len(devices),
            "deep_scan_enabled": deep_scan
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scan failed: {str(e)}")


@router.get("/last-devices")
def get_last_discovered_devices(db: Session = Depends(get_db), limit: int = 20):
    """Get recently discovered devices"""
    from ..models.appareil import Appareil
    appareils = db.query(Appareil)\
                  .order_by(Appareil.derniere_detection.desc())\
                  .limit(limit)\
                  .all()
    
    return [
        {
            "id": a.id,
            "adresse_ip": a.adresse_ip,
            "adresse_mac": a.adresse_mac,
            "marque": a.marque,
            "type_appareil": a.type_appareil.value,
            "statut": a.statut.value,
            "latence_ms": a.latence_ms,
            "derniere_detection": a.derniere_detection
        } for a in appareils
    ]