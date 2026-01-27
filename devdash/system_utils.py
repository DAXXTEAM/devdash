"""
System utilities for DevDash
"""

import platform
import os
from datetime import datetime
from typing import Dict, Optional

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False


class SystemInfo:
    """Get system information"""
    
    @staticmethod
    def get_cpu_percent() -> float:
        """Get CPU usage percentage"""
        if PSUTIL_AVAILABLE:
            return psutil.cpu_percent(interval=0.1)
        return 0.0
    
    @staticmethod
    def get_memory_info() -> Dict[str, float]:
        """Get memory usage info"""
        if PSUTIL_AVAILABLE:
            mem = psutil.virtual_memory()
            return {
                "total": mem.total / (1024 ** 3),
                "used": mem.used / (1024 ** 3),
                "free": mem.available / (1024 ** 3),
                "percent": mem.percent
            }
        return {"total": 0, "used": 0, "free": 0, "percent": 0}
    
    @staticmethod
    def get_disk_info(path: str = "/") -> Dict[str, float]:
        """Get disk usage info"""
        if PSUTIL_AVAILABLE:
            try:
                disk = psutil.disk_usage(path)
                return {
                    "total": disk.total / (1024 ** 3),
                    "used": disk.used / (1024 ** 3),
                    "free": disk.free / (1024 ** 3),
                    "percent": disk.percent
                }
            except Exception:
                pass
        return {"total": 0, "used": 0, "free": 0, "percent": 0}
    
    @staticmethod
    def get_os_info() -> Dict[str, str]:
        """Get OS information"""
        return {
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor() or "Unknown",
            "python": platform.python_version()
        }
    
    @staticmethod
    def get_uptime() -> str:
        """Get system uptime"""
        if PSUTIL_AVAILABLE:
            boot_time = datetime.fromtimestamp(psutil.boot_time())
            uptime = datetime.now() - boot_time
            days = uptime.days
            hours, remainder = divmod(uptime.seconds, 3600)
            minutes, _ = divmod(remainder, 60)
            
            parts = []
            if days > 0:
                parts.append(f"{days}d")
            if hours > 0:
                parts.append(f"{hours}h")
            parts.append(f"{minutes}m")
            
            return " ".join(parts)
        return "N/A"
    
    @staticmethod
    def get_load_average() -> tuple:
        """Get system load average"""
        try:
            return os.getloadavg()
        except (OSError, AttributeError):
            return (0.0, 0.0, 0.0)
    
    @staticmethod
    def get_process_count() -> int:
        """Get number of running processes"""
        if PSUTIL_AVAILABLE:
            return len(psutil.pids())
        return 0
    
    @staticmethod
    def get_network_io() -> Dict[str, float]:
        """Get network I/O statistics"""
        if PSUTIL_AVAILABLE:
            net = psutil.net_io_counters()
            return {
                "bytes_sent": net.bytes_sent / (1024 ** 2),
                "bytes_recv": net.bytes_recv / (1024 ** 2)
            }
        return {"bytes_sent": 0, "bytes_recv": 0}
    
    @staticmethod
    def get_battery_info() -> Optional[Dict]:
        """Get battery information if available"""
        if PSUTIL_AVAILABLE:
            try:
                battery = psutil.sensors_battery()
                if battery:
                    return {
                        "percent": battery.percent,
                        "plugged": battery.power_plugged,
                        "time_left": battery.secsleft if battery.secsleft > 0 else None
                    }
            except Exception:
                pass
        return None
    
    @staticmethod
    def get_cpu_count() -> Dict[str, int]:
        """Get CPU core count"""
        if PSUTIL_AVAILABLE:
            return {
                "physical": psutil.cpu_count(logical=False) or 0,
                "logical": psutil.cpu_count(logical=True) or 0
            }
        return {"physical": 0, "logical": 0}
    
    @staticmethod
    def get_current_user() -> str:
        """Get current username"""
        try:
            import getpass
            return getpass.getuser()
        except Exception:
            return os.environ.get("USER", "unknown")
    
    @staticmethod
    def get_hostname() -> str:
        """Get system hostname"""
        return platform.node()
