"""
Port scanning utilities for DevDash
"""

import socket
import subprocess
import platform
from typing import Dict, List, Optional

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False


class PortScanner:
    """Scan and identify running ports and services"""
    
    COMMON_PORTS = {
        22: "SSH",
        80: "HTTP",
        443: "HTTPS",
        3000: "Node/React",
        3001: "Node Dev",
        3306: "MySQL",
        5000: "Flask/Python",
        5432: "PostgreSQL",
        5173: "Vite",
        6379: "Redis",
        8000: "Django/FastAPI",
        8080: "HTTP Alt",
        8888: "Jupyter",
        9000: "PHP-FPM",
        27017: "MongoDB",
    }
    
    PROCESS_ICONS = {
        "node": "⬢",
        "python": "🐍",
        "ruby": "💎",
        "java": "☕",
        "go": "🔷",
        "rust": "🦀",
        "php": "🐘",
        "nginx": "🌐",
        "postgres": "🐘",
        "mysql": "🐬",
        "redis": "🔴",
        "mongo": "🍃",
        "docker": "🐳",
    }
    
    @classmethod
    def get_listening_ports(cls) -> List[Dict]:
        """Get all listening ports with process info"""
        ports = []
        
        if not PSUTIL_AVAILABLE:
            return cls._get_ports_fallback()
        
        try:
            connections = psutil.net_connections(kind='inet')
            
            seen_ports = set()
            for conn in connections:
                if conn.status == 'LISTEN' and conn.laddr:
                    port = conn.laddr.port
                    
                    if port in seen_ports:
                        continue
                    seen_ports.add(port)
                    
                    process_name = "Unknown"
                    process_pid = conn.pid
                    
                    if process_pid:
                        try:
                            proc = psutil.Process(process_pid)
                            process_name = proc.name()
                        except (psutil.NoSuchProcess, psutil.AccessDenied):
                            pass
                    
                    icon = cls._get_process_icon(process_name)
                    service = cls.COMMON_PORTS.get(port, process_name)
                    
                    ports.append({
                        "port": port,
                        "process": process_name,
                        "pid": process_pid,
                        "service": service,
                        "icon": icon,
                        "address": conn.laddr.ip
                    })
            
            ports.sort(key=lambda x: x["port"])
            
        except (psutil.AccessDenied, PermissionError):
            return cls._get_ports_fallback()
        
        return ports
    
    @classmethod
    def _get_ports_fallback(cls) -> List[Dict]:
        """Fallback method using netstat/ss"""
        ports = []
        system = platform.system()
        
        try:
            if system == "Linux":
                result = subprocess.run(
                    ["ss", "-tlnp"],
                    capture_output=True,
                    text=True
                )
                output = result.stdout
            elif system == "Darwin":
                result = subprocess.run(
                    ["lsof", "-iTCP", "-sTCP:LISTEN", "-n", "-P"],
                    capture_output=True,
                    text=True
                )
                output = result.stdout
            elif system == "Windows":
                result = subprocess.run(
                    ["netstat", "-ano"],
                    capture_output=True,
                    text=True
                )
                output = result.stdout
            else:
                return ports
            
            for line in output.split("\n"):
                if "LISTEN" in line or "::" in line or "0.0.0.0" in line:
                    parts = line.split()
                    for part in parts:
                        if ":" in part:
                            try:
                                port = int(part.split(":")[-1])
                                if 1 <= port <= 65535:
                                    service = cls.COMMON_PORTS.get(port, "Unknown")
                                    ports.append({
                                        "port": port,
                                        "process": "Unknown",
                                        "pid": None,
                                        "service": service,
                                        "icon": "●",
                                        "address": "0.0.0.0"
                                    })
                                    break
                            except ValueError:
                                continue
                                
        except Exception:
            pass
        
        seen = set()
        unique_ports = []
        for p in ports:
            if p["port"] not in seen:
                seen.add(p["port"])
                unique_ports.append(p)
        
        return sorted(unique_ports, key=lambda x: x["port"])
    
    @classmethod
    def _get_process_icon(cls, process_name: str) -> str:
        """Get icon for process"""
        process_lower = process_name.lower()
        for key, icon in cls.PROCESS_ICONS.items():
            if key in process_lower:
                return icon
        return "●"
    
    @classmethod
    def check_port(cls, port: int, host: str = "127.0.0.1") -> bool:
        """Check if a specific port is open"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        try:
            result = sock.connect_ex((host, port))
            return result == 0
        except Exception:
            return False
        finally:
            sock.close()
    
    @classmethod
    def find_free_port(cls, start: int = 3000, end: int = 9000) -> Optional[int]:
        """Find a free port in range"""
        for port in range(start, end):
            if not cls.check_port(port):
                return port
        return None
    
    @classmethod
    def get_port_summary(cls) -> Dict[str, int]:
        """Get summary of port usage"""
        ports = cls.get_listening_ports()
        return {
            "total": len(ports),
            "dev_ports": len([p for p in ports if p["port"] in [3000, 3001, 5000, 5173, 8000, 8080]]),
            "db_ports": len([p for p in ports if p["port"] in [3306, 5432, 6379, 27017]]),
        }
