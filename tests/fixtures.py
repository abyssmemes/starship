import shutil
import subprocess
import tempfile
from pathlib import Path

import pytest

from helpers import StarshipPromptHelper


@pytest.fixture
def prompt_helper():
    return StarshipPromptHelper()


@pytest.fixture
def git_repo():
    # Create a temporary directory for git repo
    temp_dir = tempfile.mkdtemp()
    try:
        # Initialize git repo
        subprocess.run(["git", "init", "-b", "main"], cwd=temp_dir, check=True, capture_output=True)
        subprocess.run(
            ["git", "config", "user.name", "Test User"],
            cwd=temp_dir,
            check=True,
            capture_output=True,
        )
        subprocess.run(
            ["git", "config", "user.email", "test@example.com"],
            cwd=temp_dir,
            check=True,
            capture_output=True,
        )

        # Create and add a file
        test_file = Path(temp_dir) / "test.txt"
        test_file.write_text("test content\n")
        subprocess.run(["git", "add", "test.txt"], cwd=temp_dir, check=True, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", "Initial commit"],
            cwd=temp_dir,
            check=True,
            capture_output=True,
        )

        # Create and add a file
        test_file = Path(temp_dir) / "deleted.txt"
        test_file.write_text("test content\n")
        subprocess.run(["git", "add", "deleted.txt"], cwd=temp_dir, check=True, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", "Add deleted.txt"],
            cwd=temp_dir,
            check=True,
            capture_output=True,
        )

        # Create and add a file
        test_file = Path(temp_dir) / "modified.txt"
        test_file.write_text("test content\n")
        subprocess.run(
            ["git", "add", "modified.txt"],
            cwd=temp_dir,
            check=True,
            capture_output=True,
        )
        subprocess.run(
            ["git", "commit", "-m", "Add modified.txt"],
            cwd=temp_dir,
            check=True,
            capture_output=True,
        )

        yield temp_dir
    finally:
        # Clean up
        shutil.rmtree(temp_dir)
