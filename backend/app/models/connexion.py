from sqlalchemy import Column, Integer, Enum, DateTime, ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import relationship
from ..core.database import Base
import enum

class TypeConnexion(str, enum.Enum):
    direct = "direct"
    via_switch = "via_switch"
    via_routeur = "via_routeur"
    subnet = "subnet"

class Connexion(Base):
    __tablename__ = "connexions"

    id = Column(Integer, primary_key=True, index=True)
    appareil_source_id = Column(Integer, ForeignKey("appareils.id"), nullable=False)
    appareil_destination_id = Column(Integer, ForeignKey("appareils.id"), nullable=False)
    type_connexion = Column(Enum(TypeConnexion), nullable=False)
    date_decouverte = Column(DateTime, server_default=func.now())

    # Relationships
    source = relationship("Appareil", foreign_keys=[appareil_source_id], back_populates="connexions_source")
    destination = relationship("Appareil", foreign_keys=[appareil_destination_id], back_populates="connexions_destination")

    __table_args__ = (
        UniqueConstraint('appareil_source_id', 'appareil_destination_id', name='unique_connexion'),
    )

    def __repr__(self):
        return f"<Connexion {self.appareil_source_id} → {self.appareil_destination_id}>"