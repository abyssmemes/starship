import os
import re
import subprocess
from pathlib import Path

from fixtures import git_repo, prompt_helper


def test_prompt(prompt_helper):
    result = prompt_helper.run_starship_prompt_command()

    assert result.returncode == 0

    for part in prompt_helper.get_prompt_parts(result):
        assert len(part) > 0
        assert len(part) == len(part.strip()), f"part: {part}"


def test_prompt_part_main(prompt_helper):
    env = {}

    result = prompt_helper.run_starship_prompt_command(env)
    main_part = prompt_helper.get_prompt_part(result, "main")
    main_part_parts = main_part.split(" ")

    assert len(main_part_parts) == 3

    assert os.environ["USER"] in main_part_parts[1]
    assert os.environ["PWD"].split("/")[-1] in main_part_parts[2]


def test_prompt_part_git(prompt_helper):
    result = prompt_helper.run_starship_prompt_command()
    git_part = prompt_helper.get_prompt_part(result, "git")
    git_part_parts = git_part.split(" ")

    assert len(git_part_parts) > 1


def test_prompt_part_shell(prompt_helper):
    env = {"STARSHIP_SHELL": "bash"}

    # Enabled by default
    env["STARSHIP_COCKPIT_SHELL_ENABLED"] = ""
    result = prompt_helper.run_starship_prompt_command(env)
    shell_part = prompt_helper.get_prompt_part(result, "shell")
    assert shell_part is not None

    # Disabled explicitly
    env["STARSHIP_COCKPIT_SHELL_ENABLED"] = "false"
    result = prompt_helper.run_starship_prompt_command(env)
    shell_part = prompt_helper.get_prompt_part(result, "shell")
    assert shell_part is None

    # Enabled explicitly
    env["STARSHIP_COCKPIT_SHELL_ENABLED"] = "true"
    result = prompt_helper.run_starship_prompt_command(env)
    shell_part = prompt_helper.get_prompt_part(result, "shell")

    assert shell_part == " bash"


def test_prompt_part_memory_usage(prompt_helper):
    env = {}

    # Disabled by default
    env["STARSHIP_COCKPIT_MEMORY_USAGE_ENABLED"] = ""
    result = prompt_helper.run_starship_prompt_command(env)
    memory_usage_part = prompt_helper.get_prompt_part(result, "memory_usage")
    assert memory_usage_part is None

    # Disabled explicitly
    env["STARSHIP_COCKPIT_MEMORY_USAGE_ENABLED"] = "false"
    result = prompt_helper.run_starship_prompt_command(env)
    memory_usage_part = prompt_helper.get_prompt_part(result, "memory_usage")
    assert memory_usage_part is None

    # Enabled explicitly
    env["STARSHIP_COCKPIT_MEMORY_USAGE_ENABLED"] = "true"
    result = prompt_helper.run_starship_prompt_command(env)
    memory_usage_part = prompt_helper.get_prompt_part(result, "memory_usage")
    memory_usage_part = re.sub(r"(\d+)([KMG]i?B?)/(\d+)([KMG]i?B?)", "8GiB/16GiB", memory_usage_part)

    assert memory_usage_part == "󰓅 8GiB/16GiB"


def test_prompt_part_time(prompt_helper):
    env = {}

    result = prompt_helper.run_starship_prompt_command(env=env)
    time_part = prompt_helper.get_prompt_part(result, "time")
    normalized_time = re.sub(r"(\d{1,2}):(\d{2})(?:\s*[AP]M)?", "14:30", time_part)

    assert normalized_time == "󰔛 14:30"


def test_prompt_part_git(prompt_helper, git_repo):
    env = {}

    # Run starship in the git repo
    result = prompt_helper.run_starship_prompt_command(env=env, cwd=git_repo)
    git_part = prompt_helper.get_prompt_part(result, "git")
    git_part = prompt_helper.clean_color_codes(git_part)

    assert git_part == " main"

    # Modify a file (remove line)
    modified_file = Path(git_repo) / "modified.txt"
    modified_file.write_text("")

    # Test
    result = prompt_helper.run_starship_prompt_command(env=env, cwd=git_repo)
    git_part = prompt_helper.get_prompt_part(result, "git")
    git_part = prompt_helper.clean_color_codes(git_part)

    assert git_part == " main !1 -1"

    # Modify a file (add line)
    modified_file = Path(git_repo) / "modified.txt"
    modified_file.write_text("modified content\n")

    # Test
    result = prompt_helper.run_starship_prompt_command(env=env, cwd=git_repo)
    git_part = prompt_helper.get_prompt_part(result, "git")
    git_part = prompt_helper.clean_color_codes(git_part)

    assert git_part == " main !1 +1-1"

    # Create a file
    modified_file = Path(git_repo) / "new.txt"
    modified_file.write_text("new content\n")

    # Test
    result = prompt_helper.run_starship_prompt_command(env=env, cwd=git_repo)
    git_part = prompt_helper.get_prompt_part(result, "git")
    git_part = prompt_helper.clean_color_codes(git_part)

    assert git_part == " main !1?1 +1-1"

    subprocess.run(["git", "add", "new.txt"], cwd=git_repo, check=True, capture_output=True)

    # Run starship again to check for staged changes
    result = prompt_helper.run_starship_prompt_command(env=env, cwd=git_repo)
    git_part = prompt_helper.get_prompt_part(result, "git")
    git_part = prompt_helper.clean_color_codes(git_part)

    assert git_part == " main !1+1 +1-1"

    # Remove a file
    os.remove(Path(git_repo) / "deleted.txt")

    # Run starship again to check for unstaged changes
    result = prompt_helper.run_starship_prompt_command(env=env, cwd=git_repo)
    git_part = prompt_helper.get_prompt_part(result, "git")
    git_part = prompt_helper.clean_color_codes(git_part)

    assert git_part == " main ×1!1+1 +1-2"

    # Add a file removal
    subprocess.run(["git", "add", "deleted.txt"], cwd=git_repo, check=True, capture_output=True)

    # Run starship again to check for unstaged changes
    result = prompt_helper.run_starship_prompt_command(env=env, cwd=git_repo)
    git_part = prompt_helper.get_prompt_part(result, "git")
    git_part = prompt_helper.clean_color_codes(git_part)

    assert git_part == " main ×1!1+1 +1-1"

    # Commit everything
    subprocess.run(["git", "add", "."], cwd=git_repo, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", "Commit everything"], cwd=git_repo, check=True, capture_output=True)

    # Run starship again to check for unstaged changes
    result = prompt_helper.run_starship_prompt_command(env=env, cwd=git_repo)
    git_part = prompt_helper.get_prompt_part(result, "git")
    git_part = prompt_helper.clean_color_codes(git_part)

    assert git_part == " main"

    # Create a new branch and make a commit
    subprocess.run(["git", "checkout", "-b", "feature"], cwd=git_repo, check=True, capture_output=True)
    feature_file = Path(git_repo) / "feature.txt"
    feature_file.write_text("feature content\n")
    subprocess.run(["git", "add", "feature.txt"], cwd=git_repo, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", "Add feature"], cwd=git_repo, check=True, capture_output=True)

    # Go back to main and make a different commit
    subprocess.run(["git", "checkout", "main"], cwd=git_repo, check=True, capture_output=True)
    main_file = Path(git_repo) / "main.txt"
    main_file.write_text("main content\n")
    subprocess.run(["git", "add", "main.txt"], cwd=git_repo, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", "Add main file"], cwd=git_repo, check=True, capture_output=True)

    # Create a rebase conflict situation
    subprocess.run(["git", "checkout", "feature"], cwd=git_repo, check=True, capture_output=True)
    conflict_file = Path(git_repo) / "main.txt"  # Same file as in main
    conflict_file.write_text("conflicting content\n")
    subprocess.run(["git", "add", "main.txt"], cwd=git_repo, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", "Create conflict"], cwd=git_repo, check=True, capture_output=True)

    # Start a non-interactive rebase that will cause a conflict
    subprocess.run(["git", "rebase", "main"], cwd=git_repo, capture_output=True)

    # Test
    result = prompt_helper.run_starship_prompt_command(env=env, cwd=git_repo)
    git_part = prompt_helper.get_prompt_part(result, "git")
    git_part = prompt_helper.clean_color_codes(git_part)

    normalized_git_part = re.sub(r"(@[0-9a-f]{7})", "@9ebf55a", git_part)

    assert normalized_git_part == "@9ebf55a =1 +4 REBASING 2/2"

    # Clean up the rebase (abort it)
    subprocess.run(["git", "rebase", "--abort"], cwd=git_repo, check=True, capture_output=True)
