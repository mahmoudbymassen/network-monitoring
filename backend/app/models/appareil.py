from sqlalchemy import Column, Integer, String, Enum, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from ..core.database import Base


class TypeAppareil(str, enum.Enum):
    inconnu = "inconnu"
    pc = "pc"
    routeur = "routeur"
    switch = "switch"
    camera = "camera"
    iot = "iot"
    telephone = "telephone"


class Statut(str, enum.Enum):
    en_ligne = "en_ligne"
    hors_ligne = "hors_ligne"
    inconnu = "inconnu"


class Appareil(Base):
    __tablename__ = "appareils"

    id = Column(Integer, primary_key=True, index=True)
    adresse_ip = Column(String(45), unique=True, nullable=False, index=True)
    adresse_mac = Column(String(17), unique=True)
    nom_hote = Column(String(100))
    marque = Column(String(100))
    type_appareil = Column(Enum(TypeAppareil), default=TypeAppareil.inconnu)
    etage = Column(Integer, default=1)
    sous_reseau = Column(String(18))

    statut = Column(Enum(Statut), default=Statut.inconnu)

    premier_detection = Column(DateTime, default=datetime.utcnow)
    derniere_detection = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    alertes = relationship("Alerte", back_populates="appareil", cascade="all, delete-orphan")
    resultats_scan = relationship("ResultatScan", back_populates="appareil", cascade="all, delete-orphan")
    historique_statut = relationship("HistoriqueStatut", back_populates="appareil", cascade="all, delete-orphan")
    connexions_source = relationship("Connexion", foreign_keys="Connexion.appareil_source_id", back_populates="source")
    connexions_destination = relationship("Connexion", foreign_keys="Connexion.appareil_destination_id", back_populates="destination")

    def __repr__(self):
        return f"<Appareil {self.adresse_ip}>"