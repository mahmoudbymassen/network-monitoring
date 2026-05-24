from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from ..models.appareil import TypeAppareil, Statut

class AppareilBase(BaseModel):
    adresse_ip: str
    adresse_mac: Optional[str] = None
    nom_hote: Optional[str] = None
    marque: Optional[str] = None
    type_appareil: TypeAppareil = TypeAppareil.inconnu
    etage: int = 1
    sous_reseau: Optional[str] = None
    statut: Statut = Statut.inconnu
    

class AppareilCreate(AppareilBase):
    pass

class AppareilResponse(AppareilBase):
    id: int
    premier_detection: datetime
    derniere_detection: datetime

    class Config:
        from_attributes = True   # This replaces orm_mode in Pydantic v2