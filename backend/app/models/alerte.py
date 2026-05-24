from sqlalchemy import Column, Integer, Enum, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base
import enum

class TypeAlerte(str, enum.Enum):
    nouvel_appareil = "nouvel_appareil"
    hors_ligne = "hors_ligne"
    anomalie = "anomalie"
    changement_port = "changement_port"

class Severite(str, enum.Enum):
    faible = "faible"
    moyenne = "moyenne"
    elevee = "elevee"

class Alerte(Base):
    __tablename__ = "alertes"

    id = Column(Integer, primary_key=True, index=True)
    appareil_id = Column(Integer, ForeignKey("appareils.id", ondelete="SET NULL"))
    utilisateur_id = Column(Integer, ForeignKey("utilisateurs.id", ondelete="SET NULL"))
    type_alerte = Column(Enum(TypeAlerte), nullable=False)
    severite = Column(Enum(Severite), default=Severite.moyenne)
    message = Column(Text)
    date_creation = Column(DateTime, server_default=func.now())
    accusee = Column(Boolean, default=False)

    appareil = relationship("Appareil", back_populates="alertes")

    def __repr__(self):
        return f"<Alerte {self.type_alerte} - Appareil {self.appareil_id}>"