"""
Tests for git utilities
"""

import pytest
import os
import tempfile
from devdash.git_utils import GitInfo


class TestGitInfo:
    """Test GitInfo class"""
    
    def test_non_git_repo(self):
        """Test behavior in non-git directory"""
        with tempfile.TemporaryDirectory() as tmpdir:
            git = GitInfo(tmpdir)
            assert git.is_git_repo == False
            assert git.get_branch() == "N/A"
    
    def test_get_uncommitted_count_non_repo(self):
        """Test uncommitted count in non-repo"""
        with tempfile.TemporaryDirectory() as tmpdir:
            git = GitInfo(tmpdir)
            count = git.get_uncommitted_count()
            assert count == 0
    
    def test_get_status_structure(self):
        """Test status dictionary structure"""
        git = GitInfo(".")
        status = git.get_status()
        assert "modified" in status
        assert "added" in status
        assert "deleted" in status
        assert "untracked" in status
    
    def test_get_last_commit_structure(self):
        """Test last commit dictionary structure"""
        git = GitInfo(".")
        commit = git.get_last_commit()
        assert "message" in commit
        assert "author" in commit
        assert "time" in commit
        assert "hash" in commit
    
    def test_get_remote_status_structure(self):
        """Test remote status dictionary structure"""
        git = GitInfo(".")
        remote = git.get_remote_status()
        assert "ahead" in remote
        assert "behind" in remote
    
    def test_get_today_stats_structure(self):
        """Test today stats dictionary structure"""
        git = GitInfo(".")
        stats = git.get_today_stats()
        assert "added" in stats
        assert "removed" in stats
    
    def test_get_branches_returns_list(self):
        """Test branches returns list"""
        git = GitInfo(".")
        branches = git.get_branches()
        assert isinstance(branches, list)
    
    def test_get_stash_count_returns_int(self):
        """Test stash count returns int"""
        git = GitInfo(".")
        count = git.get_stash_count()
        assert isinstance(count, int)
        assert count >= 0
