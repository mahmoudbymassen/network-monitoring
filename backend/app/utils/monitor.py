import asyncio
import time
from datetime import datetime
from typing import List
from sqlalchemy.orm import Session
from scapy.all import sr1, IP, ICMP

from ..models.appareil import Appareil, Statut
from ..models.historique_statut import HistoriqueStatut

class NetworkMonitor:

    @staticmethod
    async def ping_device(ip: str, timeout: int = 2) -> dict:
        """Ping a single device and return status + latency"""
        try:
            # Send ICMP ping
            packet = IP(dst=ip) / ICMP()
            reply = sr1(packet, timeout=timeout, verbose=False)
            
            if reply:
                # Calculate latency (approximate)
                latency = round((reply.time - packet.sent_time) * 1000, 2)
                return {
                    "status": "en_ligne",
                    "latence_ms": latency,
                    "success": True
                }
            else:
                return {
                    "status": "hors_ligne",
                    "latence_ms": None,
                    "success": False
                }
        except:
            return {
                "status": "hors_ligne",
                "latence_ms": None,
                "success": False
            }

    @staticmethod
    async def monitor_all_devices(db: Session, interval: int = 60):
        """Background task: Monitor all devices periodically"""
        print("🚀 Network Monitor started - Monitoring devices every", interval, "seconds")
        
        while True:
            try:
                appareils = db.query(Appareil).all()
                
                if not appareils:
                    await asyncio.sleep(interval)
                    continue

                print(f"📡 Monitoring {len(appareils)} devices...")

                for appareil in appareils:
                    result = await NetworkMonitor.ping_device(appareil.adresse_ip)
                    
                    old_status = appareil.statut
                    appareil.statut = Statut(result["status"])
                    appareil.latence_ms = result.get("latence_ms")
                    appareil.derniere_detection = datetime.utcnow()

                    # Create alert if device just went offline
                    if old_status == Statut.en_ligne and appareil.statut == Statut.hors_ligne:
                        from ..models.alerte import TypeAlerte, Severite, Alerte
                        alert = Alerte(
                            appareil_id=appareil.id,
                            type_alerte=TypeAlerte.hors_ligne,
                            severite=Severite.elevee,
                            message=f"Appareil hors ligne: {appareil.adresse_ip} ({appareil.nom_hote or 'Unknown'})"
                        )
                        db.add(alert)
                        print(f"🚨 ALERT: {appareil.adresse_ip} went OFFLINE!")

                db.commit()
                print(f"✅ Monitoring cycle completed at {datetime.now().strftime('%H:%M:%S')}")

            except Exception as e:
                print(f"⚠️ Error in monitoring loop: {e}")

            await asyncio.sleep(interval)

    @staticmethod
    def start_monitoring(db: Session, interval: int = 60):
        """Start the monitoring loop in background"""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(NetworkMonitor.monitor_all_devices(db, interval))