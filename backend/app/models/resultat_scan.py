from sqlalchemy import Column, Integer, JSON, Float, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base

class ResultatScan(Base):
    __tablename__ = "resultats_scan"

    id = Column(Integer, primary_key=True, index=True)
    appareil_id = Column(Integer, ForeignKey("appareils.id"), nullable=False)
    scan_id = Column(Integer, ForeignKey("scans.id"))
    ports_ouverts = Column(JSON)
    services = Column(JSON)
    os_detection = Column(String(100))
    latence_ms = Column(Float, nullable=True)
    date_scan = Column(DateTime, server_default=func.now())

    # Relationship
    appareil = relationship("Appareil", back_populates="resultats_scan")

    def __repr__(self):
        return f"<ResultatScan(appareil_id={self.appareil_id})>"