from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey
from sqlalchemy.sql import func
from ..core.database import Base
import enum

class TypeScan(str, enum.Enum):
    decouverte = "decouverte"
    ports = "ports"
    monitoring = "monitoring"

class Scan(Base):
    __tablename__ = "scans"

    id = Column(Integer, primary_key=True, index=True)
    type_scan = Column(Enum(TypeScan), nullable=False)
    plage_cible = Column(String(50))
    date_debut = Column(DateTime)
    date_fin = Column(DateTime)
    appareils_trouves = Column(Integer, default=0)
    utilisateur_id = Column(Integer, ForeignKey("utilisateurs.id", ondelete="SET NULL"))

    def __repr__(self):
        return f"<Scan {self.type_scan} - {self.plage_cible}>"