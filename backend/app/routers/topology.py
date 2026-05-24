from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from collections import defaultdict
from typing import Dict, List

from ..core.database import get_db
from ..models.appareil import Appareil

router = APIRouter()

@router.get("/")
async def get_topology(db: Session = Depends(get_db)):
    """Professional Multi-Floor Network Topology"""
    
    appareils = db.query(Appareil).all()
    
    nodes = []
    edges = []
    floors = defaultdict(list)

    # Create Nodes
    for appareil in appareils:
        node = {
            "id": appareil.id,
            "ip": appareil.adresse_ip,
            "mac": appareil.adresse_mac,
            "label": appareil.nom_hote or appareil.adresse_ip,
            "marque": appareil.marque or "Unknown",
            "type": appareil.type_appareil.value,
            "status": appareil.statut.value,
            "floor": appareil.etage,
            "last_seen": appareil.derniere_detection.isoformat() if appareil.derniere_detection else None,
            "icon": get_icon(appareil.type_appareil.value)
        }
        nodes.append(node)
        floors[appareil.etage].append(node)

    # === Smart Connection Logic ===
    core_id = 9999
    
    # Add Virtual Core Router
    nodes.append({
        "id": core_id,
        "ip": "192.168.1.1",
        "label": "Core Router / Switch Principal",
        "type": "routeur",
        "status": "en_ligne",
        "floor": 0,
        "is_virtual": True,
        "icon": "router"
    })

    # Connect devices intelligently
    for appareil in appareils:
        # Connect every device to Core
        edges.append({
            "from": appareil.id,
            "to": core_id,
            "type": "to_core",
            "label": "Uplink"
        })

        # Connect devices on same floor (simulated LAN)
        for other in floors[appareil.etage]:
            if other["id"] != appareil.id:
                edges.append({
                    "from": appareil.id,
                    "to": other["id"],
                    "type": "same_floor",
                    "label": "LAN"
                })

    return {
        "status": "success",
        "topology": {
            "nodes": nodes,
            "edges": edges
        },
        "floors": {
            floor: {
                "count": len(devices),
                "devices": devices
            } for floor, devices in floors.items()
        },
        "summary": {
            "total_devices": len(appareils),
            "online_devices": len([a for a in appareils if a.statut == "en_ligne"]),
            "floors_count": len(floors),
            "connections_count": len(edges)
        },
        "last_updated": "now"
    }


def get_icon(device_type: str) -> str:
    icons = {
        "routeur": "router",
        "switch": "switch",
        "pc": "pc",
        "camera": "camera",
        "iot": "iot",
        "inconnu": "unknown"
    }
    return icons.get(device_type, "unknown")