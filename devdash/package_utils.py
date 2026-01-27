"""
Package management utilities for DevDash
"""

import os
import json
import subprocess
from typing import Dict, List, Optional
from pathlib import Path


class PackageInfo:
    """Check for outdated packages"""
    
    @staticmethod
    def detect_project_type(path: str = ".") -> Optional[str]:
        """Detect project type based on config files"""
        path = Path(path)
        
        if (path / "package.json").exists():
            return "node"
        elif (path / "requirements.txt").exists():
            return "python-pip"
        elif (path / "pyproject.toml").exists():
            return "python-poetry"
        elif (path / "Cargo.toml").exists():
            return "rust"
        elif (path / "go.mod").exists():
            return "go"
        elif (path / "Gemfile").exists():
            return "ruby"
        elif (path / "composer.json").exists():
            return "php"
        
        return None
    
    @staticmethod
    def get_node_outdated(path: str = ".") -> List[Dict]:
        """Get outdated npm packages"""
        outdated = []
        
        try:
            result = subprocess.run(
                ["npm", "outdated", "--json"],
                cwd=path,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.stdout:
                data = json.loads(result.stdout)
                for name, info in data.items():
                    outdated.append({
                        "name": name,
                        "current": info.get("current", "?"),
                        "wanted": info.get("wanted", "?"),
                        "latest": info.get("latest", "?"),
                        "type": "npm"
                    })
        except Exception:
            pass
        
        return outdated[:10]
    
    @staticmethod
    def get_python_outdated(path: str = ".") -> List[Dict]:
        """Get outdated pip packages"""
        outdated = []
        
        try:
            result = subprocess.run(
                ["pip", "list", "--outdated", "--format=json"],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.stdout:
                data = json.loads(result.stdout)
                for pkg in data[:10]:
                    outdated.append({
                        "name": pkg.get("name", "?"),
                        "current": pkg.get("version", "?"),
                        "wanted": pkg.get("latest_version", "?"),
                        "latest": pkg.get("latest_version", "?"),
                        "type": "pip"
                    })
        except Exception:
            pass
        
        return outdated
    
    @classmethod
    def get_outdated_packages(cls, path: str = ".") -> List[Dict]:
        """Get outdated packages based on project type"""
        project_type = cls.detect_project_type(path)
        
        if project_type == "node":
            return cls.get_node_outdated(path)
        elif project_type in ["python-pip", "python-poetry"]:
            return cls.get_python_outdated(path)
        
        return []
    
    @staticmethod
    def get_package_count(path: str = ".") -> Dict[str, int]:
        """Get count of installed packages"""
        path = Path(path)
        result = {"dependencies": 0, "dev_dependencies": 0}
        
        package_json = path / "package.json"
        if package_json.exists():
            try:
                with open(package_json) as f:
                    data = json.load(f)
                    result["dependencies"] = len(data.get("dependencies", {}))
                    result["dev_dependencies"] = len(data.get("devDependencies", {}))
            except Exception:
                pass
        
        return result
    
    @staticmethod
    def get_project_scripts(path: str = ".") -> Dict[str, str]:
        """Get npm scripts from package.json"""
        path = Path(path)
        package_json = path / "package.json"
        
        if package_json.exists():
            try:
                with open(package_json) as f:
                    data = json.load(f)
                    return data.get("scripts", {})
            except Exception:
                pass
        
        return {}
