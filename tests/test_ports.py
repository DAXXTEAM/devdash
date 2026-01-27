"""
Tests for port utilities
"""

import pytest
from devdash.port_utils import PortScanner


class TestPortScanner:
    """Test PortScanner class"""
    
    def test_get_listening_ports_returns_list(self):
        """Test that get_listening_ports returns a list"""
        ports = PortScanner.get_listening_ports()
        assert isinstance(ports, list)
    
    def test_port_structure(self):
        """Test port dictionary structure"""
        ports = PortScanner.get_listening_ports()
        if ports:
            port = ports[0]
            assert "port" in port
            assert "process" in port
            assert "service" in port
            assert "icon" in port
    
    def test_check_port_closed(self):
        """Test checking a likely closed port"""
        result = PortScanner.check_port(59999)
        assert isinstance(result, bool)
    
    def test_find_free_port(self):
        """Test finding a free port"""
        port = PortScanner.find_free_port(40000, 50000)
        if port:
            assert 40000 <= port < 50000
    
    def test_get_port_summary(self):
        """Test port summary structure"""
        summary = PortScanner.get_port_summary()
        assert "total" in summary
        assert "dev_ports" in summary
        assert "db_ports" in summary
        assert isinstance(summary["total"], int)
    
    def test_common_ports_dict(self):
        """Test common ports dictionary"""
        assert 80 in PortScanner.COMMON_PORTS
        assert 443 in PortScanner.COMMON_PORTS
        assert 5432 in PortScanner.COMMON_PORTS
        assert PortScanner.COMMON_PORTS[80] == "HTTP"
