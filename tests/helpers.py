import os
import re
import subprocess

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
        prompt_env = {}
        prompt_env["PWD"] = cwd if cwd else BASE_DIR
        prompt_env["STARSHIP_SHELL"] = os.environ.get("STARSHIP_SHELL", "bash")
        if env:
            prompt_env.update(env)
        result = self.run_starship_command(["prompt"], prompt_env, cwd=cwd)
        self.print_prompt_debug(result)
        return result

    def clean_output(self, output):
        output = output.replace("\\[", "")
        output = output.replace("\\]", "")
        output = output.replace("%{", "")
        output = output.replace("%}", "")
        return output

    def clean_color_codes(self, output):
        return re.sub(r"\x1b\[[0-9;]*m", "", output)

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
        print(f"{header} {divider}{parts[0]}")
        for part in parts[1:]:
            spacer = " " * len(header)
            print(f"{spacer} {divider}{part}")

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
