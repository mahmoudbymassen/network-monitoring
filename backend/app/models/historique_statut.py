from sqlalchemy import Column, Integer, Enum, Float, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from ..core.database import Base
import enum

class Statut(str, enum.Enum):
    en_ligne = "en_ligne"
    hors_ligne = "hors_ligne"
    inconnu = "inconnu"

class HistoriqueStatut(Base):
    __tablename__ = "historique_statut"

    id = Column(Integer, primary_key=True, index=True)
    appareil_id = Column(Integer, ForeignKey("appareils.id"), nullable=False)
    statut = Column(Enum(Statut), nullable=False)
    latence_ms = Column(Float, nullable=True)
    date_enregistrement = Column(DateTime, server_default=func.now())

    # Relationship
    appareil = relationship("Appareil", back_populates="historique_statut")

    def __repr__(self):
        return f"<HistoriqueStatut appareil={self.appareil_id} statut={self.statut}>"