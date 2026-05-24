from scapy.all import srp, Ether, ARP
import nmap
import asyncio
import subprocess

from typing import List, Dict
from datetime import datetime
from sqlalchemy.orm import Session

from ..models.appareil import Appareil, TypeAppareil, Statut
from ..models.alerte import Alerte, TypeAlerte, Severite


class NetworkScanner:

    # =========================================================
    # NETWORK DISCOVERY - IMPROVED
    # =========================================================
    @staticmethod
    async def arp_scan(ip_range: str = "192.168.1.0/24") -> List[Dict]:
        """Strong Hostname + MAC detection"""
        print(f"🔍 Starting Enhanced Scan on {ip_range}...")

        devices = []
        seen_ips = set()

        # 1. ARP Scan
        try:
            ans, _ = srp(Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip_range), 
                         timeout=4, verbose=False)
            for _, received in ans:
                ip = received.psrc
                mac = received.src.upper()
                if ip not in seen_ips:
                    devices.append({
                        "adresse_ip": ip,
                        "adresse_mac": mac,
                        "nom_hote": "Unknown",
                        "source": "arp"
                    })
                    seen_ips.add(ip)
        except:
            pass

        # 2. Local ARP Cache
        try:
            result = subprocess.run(['arp', '-a'], capture_output=True, text=True, timeout=5)
            for line in result.stdout.splitlines():
                if any(x in line.lower() for x in ['dynamic', 'static']):
                    parts = line.strip().split()
                    if len(parts) >= 3 and parts[0].count('.') == 3:
                        ip = parts[0]
                        mac = parts[1].replace('-', ':').upper()
                        if ip not in seen_ips:
                            devices.append({
                                "adresse_ip": ip,
                                "adresse_mac": mac,
                                "nom_hote": "Unknown",
                                "source": "arp_cache"
                            })
                            seen_ips.add(ip)
        except:
            pass

        # 3. Hostname Resolution (Improved)
        print("🔍 Trying to resolve hostnames...")
        import socket
        for device in devices:
            ip = device["adresse_ip"]
            hostname = "Unknown"

            # Method A: Socket gethostbyaddr
            try:
                hostname = socket.gethostbyaddr(ip)[0]
                print(f"✅ DNS Hostname: {ip} → {hostname}")
            except:
                pass

            # Method B: nbtstat (Best for Windows devices)
            if hostname == "Unknown":
                try:
                    result = subprocess.run(['nbtstat', '-A', ip], 
                                          capture_output=True, text=True, timeout=3)
                    for line in result.stdout.splitlines():
                        if '<00>' in line and 'UNIQUE' in line.upper():
                            parts = line.strip().split()
                            if len(parts) > 0:
                                hostname = parts[0]
                                print(f"✅ NetBIOS Hostname: {ip} → {hostname}")
                                break
                except:
                    pass

            device["nom_hote"] = hostname

        print(f"📊 Total devices found: {len(devices)}")
        for d in devices[:10]:   # Show first 10 for debugging
            print(f"   {d['adresse_ip']} | {d.get('adresse_mac','--')} | {d.get('nom_hote','Unknown')}")

        return devices
    # =========================================================
    # DEEP SCAN (Nmap)
    # =========================================================
    @staticmethod
    def deep_scan(ip: str) -> Dict:
        try:
            nm = nmap.PortScanner()
            nm.scan(hosts=ip, arguments='-sS -O -T4 --open')

            if ip not in nm.all_hosts():
                return {"ports": [], "os": "Unknown", "services": {}}

            host = nm[ip]
            open_ports = list(host['tcp'].keys()) if 'tcp' in host else []

            services = {port: host['tcp'][port].get('name', 'unknown') for port in open_ports}

            os_match = "Unknown"
            if 'osmatch' in host and host['osmatch']:
                os_match = host['osmatch'][0]['name']

            return {
                "ports": open_ports,
                "os": os_match,
                "services": services
            }

        except Exception as e:
            print(f"Nmap scan error on {ip}: {e}")
            return {"ports": [], "os": "Unknown", "services": {}}


    # =========================================================
    # CLASSIFY DEVICE
    # =========================================================
    @staticmethod
    def classify_device(mac: str, scan_result: Dict = None) -> Dict:
        marque = "Unknown"

        try:
            from mac_vendor_lookup import MacLookup
            marque = MacLookup().lookup(mac)
        except:
            pass

        device_type = TypeAppareil.inconnu
        m = marque.lower()

        if any(x in m for x in ['cisco', 'tp-link', 'netgear', 'huawei', 'd-link']):
            device_type = TypeAppareil.routeur
        elif any(x in m for x in ['hikvision', 'dahua', 'reolink']):
            device_type = TypeAppareil.camera
        elif any(x in m for x in ['hp', 'dell', 'lenovo', 'asus', 'apple', 'macbook']):
            device_type = TypeAppareil.pc
        elif any(x in m for x in ['samsung', 'xiaomi', 'huawei', 'oppo']):
            device_type = TypeAppareil.iot

        return {
            "marque": marque,
            "type_appareil": device_type,
            "os": scan_result.get("os", "Unknown") if scan_result else "Unknown"
        }


    # =========================================================
    # SAVE DEVICES TO DATABASE
    # =========================================================
    @staticmethod
    async def save_discovered_devices(
        devices: List[Dict],
        db: Session,
        deep_scan_enabled: bool = False
    ):
        print("💾 Updating database...")

        # Mark all as offline first
        db.query(Appareil).update({Appareil.statut: Statut.hors_ligne})

        count_new = 0

        for dev in devices:
            ip = dev["adresse_ip"]
            mac = dev.get("adresse_mac")
            if mac == "Unknown":
                mac = None

            scan_result = None
            if deep_scan_enabled:
                scan_result = NetworkScanner.deep_scan(ip)

            classification = NetworkScanner.classify_device(mac or "Unknown", scan_result)

            # Check if device exists by IP or MAC
            existing = db.query(Appareil).filter(Appareil.adresse_ip == ip).first()
            if not existing and mac:
                existing = db.query(Appareil).filter(Appareil.adresse_mac == mac).first()

            if existing:
                # Update existing device
                existing.adresse_ip = ip
                existing.adresse_mac = mac
                existing.marque = classification["marque"]
                existing.type_appareil = classification["type_appareil"]
                existing.statut = Statut.en_ligne
                existing.derniere_detection = datetime.utcnow()
                print(f"🟢 Updated: {ip} - {classification['marque']}")
            else:
                # Create new device
                new_device = Appareil(
                    adresse_ip=ip,
                    adresse_mac=mac,
                    marque=classification["marque"],
                    type_appareil=classification["type_appareil"],
                    statut=Statut.en_ligne,
                    derniere_detection=datetime.utcnow()
                )
                db.add(new_device)
                db.flush()

                # Create alert for new device
                alert = Alerte(
                    appareil_id=new_device.id,
                    type_alerte=TypeAlerte.nouvel_appareil,
                    severite=Severite.moyenne,
                    message=f"Nouvel appareil détecté: {ip} ({classification['marque']})"
                )
                db.add(alert)
                count_new += 1
                print(f"🆕 New Device: {ip}")

        db.commit()
        print(f"✅ Saved/Updated {len(devices)} devices ({count_new} new)")