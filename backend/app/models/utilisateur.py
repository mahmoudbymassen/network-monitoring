from sqlalchemy import Column, Integer, String, Enum, Boolean, DateTime
from sqlalchemy.sql import func
from ..core.database import Base
import enum

class Role(str, enum.Enum):
    admin = "admin"
    utilisateur = "utilisateur"

class Utilisateur(Base):
    __tablename__ = "utilisateurs"

    id = Column(Integer, primary_key=True, index=True)
    nom_utilisateur = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    mot_de_passe = Column(String(255), nullable=False)
    role = Column(Enum(Role), default=Role.utilisateur)
    actif = Column(Boolean, default=True)
    date_creation = Column(DateTime, server_default=func.now())
    derniere_connexion = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"<Utilisateur {self.nom_utilisateur} ({self.role})>"