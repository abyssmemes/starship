import os
import re
import subprocess
import tempfile

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

COLOR_CODE_PATTERN = r"\x1b\[[0-9;]*m"


class StarshipPromptHelper:
    def __init__(self):
        self.config_path = os.path.join(BASE_DIR, "starship.toml")
        os.environ["STARSHIP_CONFIG"] = self.config_path

    def run_starship_command(self, args, env=None, cwd=None):
        cmd = ["starship"] + args
        custom_env = os.environ.copy()
        if env:
            custom_env.update(env)
        result = subprocess.run(cmd, env=custom_env, capture_output=True, text=True, cwd=cwd)
        return result

    def run_starship_prompt_command(self, env=None, cwd=None):
        prompt_env = os.environ.copy()
        prompt_env["PWD"] = cwd if cwd else BASE_DIR
        prompt_env["STARSHIP_SHELL"] = prompt_env.get("STARSHIP_SHELL", "bash")
        if env:
            prompt_env.update(env)

        # On Windows, we need a different approach
        if os.name == "nt":
            # Use direct command execution with output redirection
            cmd = "starship prompt"
            # Create a temporary batch file to run the command
            with tempfile.NamedTemporaryFile(suffix=".bat", delete=False, mode="w") as f:
                f.write(f"@echo off\n{cmd}")
                batch_file = f.name

            try:
                result = subprocess.run(
                    [batch_file],
                    env=prompt_env,
                    cwd=cwd,
                    text=True,
                    capture_output=True,
                    encoding="utf-8",
                    errors="replace",
                )
            finally:
                os.unlink(batch_file)
        else:
            # Unix systems work fine with the standard approach
            result = subprocess.run(
                ["starship", "prompt"],
                env=prompt_env,
                cwd=cwd,
                text=True,
                capture_output=True,
                encoding="utf-8",
                errors="replace",
            )

        self.print_prompt_debug(result)
        return result

    def clean_output(self, output):
        output = output.replace("\\[", "")
        output = output.replace("\\]", "")
        output = output.replace("%{", "")
        output = output.replace("%}", "")
        return output

    def clean_color_codes(self, output):
        # First remove ANSI color codes
        output = re.sub(COLOR_CODE_PATTERN, "", output)

        # If we're on Windows, also replace problematic Unicode characters
        if os.name == "nt":
            # Replace any non-ASCII characters with simple placeholders
            def replace_non_ascii(match):
                return f"[icon]"

            # Replace any character outside the ASCII range
            output = re.sub(r"[^\x00-\x7F]+", replace_non_ascii, output)

        return output

    def get_prompt(self, result):
        return self.clean_output(result.stdout.strip())

    def get_prompt_lines(self, result):
        prompt = self.get_prompt(result)
        prompt_lines = [line.strip() for line in prompt.split("\n")]
        return prompt_lines

    def get_prompt_parts(self, result):
        prompt_lines = self.get_prompt_lines(result)
        prompt_parts = prompt_lines[0].split("  ")
        return prompt_parts

    def get_prompt_part(self, prompt, part_name):
        prompt_parts = self.get_prompt_parts(prompt)
        if part_name == "main":
            return prompt_parts[0]
        for part in prompt_parts:
            clean_part = self.clean_color_codes(part)
            if any(
                [
                    part_name == "git" and (clean_part.startswith("") or clean_part.startswith("@")),
                    part_name == "shell" and clean_part.startswith(""),
                    part_name == "memory_usage" and clean_part.startswith("󰓅"),
                    part_name == "time" and clean_part.startswith("󰔛"),
                ]
            ):
                return part
        return None

    def print_prompt_debug(self, result):
        self.print_spacer()
        self.print_spacer()
        self.print_prompt(result)
        self.print_spacer()
        self.print_prompt_parts(result)
        self.print_spacer()

    def print_parts(self, parts, header):
        divider = "┆"
        try:
            print(f"{header} {divider}{parts[0]}")
            for part in parts[1:]:
                spacer = " " * len(header)
                print(f"{spacer} {divider}{part}")
        except UnicodeEncodeError:
            # Fall back to ASCII-only output if the terminal can't handle Unicode
            safe_divider = "|"
            print(f"{header} {safe_divider}{self.clean_color_codes(parts[0])}")
            for part in parts[1:]:
                spacer = " " * len(header)
                print(f"{spacer} {safe_divider}{self.clean_color_codes(part)}")

    def print_prompt(self, result):
        prompt_lines = self.get_prompt_lines(result)
        header = "PROMPT"
        self.print_parts(prompt_lines, header)

    def print_prompt_parts(self, result):
        prompt_parts = self.get_prompt_parts(result)
        header = "PARTS "
        self.print_parts(prompt_parts, header)

    def print_spacer(self):
        print("")
