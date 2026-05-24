from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime

class DashboardStats(BaseModel):
    total_appareils: int
    en_ligne: int
    hors_ligne: int
    pourcentage_en_ligne: float
    
    par_etage: Dict[str, int]
    par_type: Dict[str, int]
    
    last_scan: Optional[datetime]
    recent_alerts: int
    last_alert: Optional[dict]