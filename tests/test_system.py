"""
Tests for system utilities
"""

import pytest
from devdash.system_utils import SystemInfo


class TestSystemInfo:
    """Test SystemInfo class"""
    
    def test_get_cpu_percent(self):
        """Test CPU percentage is valid"""
        cpu = SystemInfo.get_cpu_percent()
        assert isinstance(cpu, float)
        assert 0 <= cpu <= 100
    
    def test_get_memory_info(self):
        """Test memory info structure"""
        mem = SystemInfo.get_memory_info()
        assert "total" in mem
        assert "used" in mem
        assert "free" in mem
        assert "percent" in mem
        assert mem["total"] > 0
    
    def test_get_disk_info(self):
        """Test disk info structure"""
        disk = SystemInfo.get_disk_info()
        assert "total" in disk
        assert "used" in disk
        assert "free" in disk
        assert "percent" in disk
    
    def test_get_os_info(self):
        """Test OS info structure"""
        os_info = SystemInfo.get_os_info()
        assert "system" in os_info
        assert "release" in os_info
        assert "python" in os_info
        assert os_info["system"] in ["Linux", "Darwin", "Windows"]
    
    def test_get_uptime(self):
        """Test uptime returns string"""
        uptime = SystemInfo.get_uptime()
        assert isinstance(uptime, str)
    
    def test_get_process_count(self):
        """Test process count is positive"""
        count = SystemInfo.get_process_count()
        assert isinstance(count, int)
        assert count >= 0
    
    def test_get_hostname(self):
        """Test hostname returns string"""
        hostname = SystemInfo.get_hostname()
        assert isinstance(hostname, str)
        assert len(hostname) > 0
    
    def test_get_current_user(self):
        """Test current user returns string"""
        user = SystemInfo.get_current_user()
        assert isinstance(user, str)
        assert len(user) > 0
