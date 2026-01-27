"""
Git utilities for DevDash
"""

import subprocess
import os
from datetime import datetime
from typing import Dict, List, Optional, Tuple


class GitInfo:
    """Get git repository information"""
    
    def __init__(self, path: str = "."):
        self.path = os.path.abspath(path)
        self.is_git_repo = self._check_git_repo()
    
    def _check_git_repo(self) -> bool:
        """Check if current directory is a git repo"""
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--git-dir"],
                cwd=self.path,
                capture_output=True,
                text=True
            )
            return result.returncode == 0
        except FileNotFoundError:
            return False
    
    def _run_git(self, *args) -> Tuple[bool, str]:
        """Run a git command and return output"""
        try:
            result = subprocess.run(
                ["git"] + list(args),
                cwd=self.path,
                capture_output=True,
                text=True
            )
            return result.returncode == 0, result.stdout.strip()
        except Exception:
            return False, ""
    
    def get_branch(self) -> str:
        """Get current branch name"""
        if not self.is_git_repo:
            return "N/A"
        success, output = self._run_git("branch", "--show-current")
        return output if success and output else "detached"
    
    def get_status(self) -> Dict[str, int]:
        """Get git status summary"""
        status = {"modified": 0, "added": 0, "deleted": 0, "untracked": 0}
        if not self.is_git_repo:
            return status
        
        success, output = self._run_git("status", "--porcelain")
        if not success:
            return status
        
        for line in output.split("\n"):
            if not line:
                continue
            code = line[:2]
            if "M" in code:
                status["modified"] += 1
            elif "A" in code:
                status["added"] += 1
            elif "D" in code:
                status["deleted"] += 1
            elif "?" in code:
                status["untracked"] += 1
        
        return status
    
    def get_last_commit(self) -> Dict[str, str]:
        """Get last commit info"""
        if not self.is_git_repo:
            return {"message": "N/A", "author": "N/A", "time": "N/A", "hash": "N/A"}
        
        success, output = self._run_git(
            "log", "-1", "--format=%h|%s|%an|%ar"
        )
        
        if not success or not output:
            return {"message": "No commits", "author": "N/A", "time": "N/A", "hash": "N/A"}
        
        parts = output.split("|")
        if len(parts) >= 4:
            return {
                "hash": parts[0],
                "message": parts[1][:50] + ("..." if len(parts[1]) > 50 else ""),
                "author": parts[2],
                "time": parts[3]
            }
        return {"message": "N/A", "author": "N/A", "time": "N/A", "hash": "N/A"}
    
    def get_remote_status(self) -> Dict[str, int]:
        """Get ahead/behind status from remote"""
        result = {"ahead": 0, "behind": 0}
        if not self.is_git_repo:
            return result
        
        self._run_git("fetch", "--quiet")
        
        success, output = self._run_git(
            "rev-list", "--left-right", "--count", "@{upstream}...HEAD"
        )
        
        if success and output:
            parts = output.split()
            if len(parts) >= 2:
                result["behind"] = int(parts[0])
                result["ahead"] = int(parts[1])
        
        return result
    
    def get_uncommitted_count(self) -> int:
        """Get count of uncommitted changes"""
        status = self.get_status()
        return sum(status.values())
    
    def get_repo_name(self) -> str:
        """Get repository name"""
        if not self.is_git_repo:
            return os.path.basename(self.path)
        
        success, output = self._run_git("remote", "get-url", "origin")
        if success and output:
            name = output.split("/")[-1]
            return name.replace(".git", "")
        
        return os.path.basename(self.path)
    
    def get_today_commits(self) -> int:
        """Get number of commits made today"""
        if not self.is_git_repo:
            return 0
        
        today = datetime.now().strftime("%Y-%m-%d")
        success, output = self._run_git(
            "log", "--oneline", f"--since={today} 00:00:00"
        )
        
        if success and output:
            return len(output.strip().split("\n"))
        return 0
    
    def get_today_stats(self) -> Dict[str, int]:
        """Get lines added/removed today"""
        result = {"added": 0, "removed": 0}
        if not self.is_git_repo:
            return result
        
        today = datetime.now().strftime("%Y-%m-%d")
        success, output = self._run_git(
            "log", "--numstat", "--format=", f"--since={today} 00:00:00"
        )
        
        if success and output:
            for line in output.strip().split("\n"):
                parts = line.split()
                if len(parts) >= 2:
                    try:
                        if parts[0] != "-":
                            result["added"] += int(parts[0])
                        if parts[1] != "-":
                            result["removed"] += int(parts[1])
                    except ValueError:
                        pass
        
        return result
    
    def get_branches(self) -> List[str]:
        """Get list of local branches"""
        if not self.is_git_repo:
            return []
        
        success, output = self._run_git("branch", "--format=%(refname:short)")
        if success and output:
            return output.strip().split("\n")
        return []
    
    def get_stash_count(self) -> int:
        """Get number of stashes"""
        if not self.is_git_repo:
            return 0
        
        success, output = self._run_git("stash", "list")
        if success and output:
            return len(output.strip().split("\n"))
        return 0
