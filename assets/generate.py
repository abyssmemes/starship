import os
import time
from PIL import ImageGrab
import applescript
import signal

WINDOW_WIDTH = 870
WINDOW_HEIGHT = 460
WINDOW_HEIGHT_SINGLE = 105

DEFAULT_ITERM_COLORS = "Cockpit-Tokyo-Night"
DEFAULT_PALETTE = "default"


def scene_init():
    return [

        # ********************************************************************
        # **** Init **********************************************************
        # ********************************************************************

        # ---- Open iTerm ----------------------------------------------------
        *actions_iterm_open(),
        *actions_colors(DEFAULT_ITERM_COLORS, DEFAULT_PALETTE),
        *actions_iterm_window_size(WINDOW_WIDTH, WINDOW_HEIGHT),
        # ---- Prepare -------------------------------------------------------
        *actions_command_list([
            "export DISABLE_AUTO_TITLE=true",
            "export STARSHIP_COCKPIT_MEMORY_USAGE_ENABLED=false",
            "export STARSHIP_COCKPIT_BATTERY_ENABLED=false",
            "export STARSHIP_COCKPIT_BATTERY_THRESHOLD=100",
            "export STARSHIP_COCKPIT_KEYBOARD_LAYOUT_ENABLED=false",
            "export STARSHIP_COCKPIT_KEYBOARD_LAYOUT_ABC=ENG",
            "export STARSHIP_COCKPIT_KEYBOARD_LAYOUT_UKRAINIAN=UKR",
        ]),
        *actions_clear(),
    ]

def scene_demo():
    return [

        # ********************************************************************
        # **** Demo **********************************************************
        # ********************************************************************

        # ---- Set color scheme ----------------------------------------------
        *actions_colors(DEFAULT_ITERM_COLORS, DEFAULT_PALETTE),
        # ---- Prepare -------------------------------------------------------
        *actions_command_list([
            f"cd {os.getcwd()}",
            "git clone https://github.com/smithumble/starship-cockpit.git",
            "mv starship-cockpit starship-cockpit-demo",
            "cd starship-cockpit-demo",
            "touch docker-compose.yml",
            "export DOCKER_CONTEXT=dev",
        ]),
        *actions_iterm_window_size(WINDOW_WIDTH, WINDOW_HEIGHT),
        *actions_clear(),
        # ---- Run commands --------------------------------------------------
        *actions_command_list([
            "git reset --hard HEAD~1 -q",
            "echo 'Hello, World!' > NEW_FILE.md",
            "git add NEW_FILE.md",
            "git commit -m 'Add NEW_FILE.md' -q",
            "rm NEW_FILE.md",
            "echo 'Hello, World!' > README.md",
        ], command_delay=1, delay_before=1, delay_after=1),
        *actions_command_list([
            "sleep 2",
        ], delay_after=3),
        *actions_command_list([
            "test",
        ]),
        # ---- Make screenshot -----------------------------------------------
        *actions_screenshot("assets/demo.png"),
        # ---- Cleanup -------------------------------------------------------
        *actions_iterm_window_size(WINDOW_WIDTH, WINDOW_HEIGHT),
        *actions_clear(),
    ]

def scene_palettes():
    return [

        # ********************************************************************
        # **** Palettes ******************************************************
        # ********************************************************************

        # ====================================================================
        # ==== Tokyo Night ===================================================
        # ====================================================================
        # ---- Set color scheme ----------------------------------------------
        *actions_colors("Tokyo-Night", "default"),
        # ---- Prepare -------------------------------------------------------
        *actions_iterm_window_size(WINDOW_WIDTH, WINDOW_HEIGHT_SINGLE),
        *actions_clear(),
        # ---- Make screenshot -----------------------------------------------
        *actions_screenshot("assets/palettes/default.png"),
        # ---- Cleanup -------------------------------------------------------
        *actions_iterm_window_size(WINDOW_WIDTH, WINDOW_HEIGHT),
        *actions_clear(),

        # ====================================================================
        # ==== Gruvbox Dark ==================================================
        # ====================================================================
        # ---- Set color scheme ----------------------------------------------
        *actions_colors("Cockpit-Gruvbox-Dark", "gruvbox_dark"),
        # ---- Prepare -------------------------------------------------------
        *actions_iterm_window_size(WINDOW_WIDTH, WINDOW_HEIGHT_SINGLE),
        *actions_clear(),
        # ---- Make screenshot -----------------------------------------------
        *actions_screenshot("assets/palettes/gruvbox_dark.png"),
        # ---- Cleanup -------------------------------------------------------
        *actions_iterm_window_size(WINDOW_WIDTH, WINDOW_HEIGHT),
        *actions_clear(),

        # ====================================================================
        # ==== Gruvbox Light =================================================
        # ====================================================================
        # ---- Set color scheme ----------------------------------------------
        *actions_colors("Cockpit-Gruvbox-Light", "gruvbox_light"),
        # ---- Prepare -------------------------------------------------------
        *actions_iterm_window_size(WINDOW_WIDTH, WINDOW_HEIGHT_SINGLE),
        *actions_clear(),
        # ---- Make screenshot -----------------------------------------------
        *actions_screenshot("assets/palettes/gruvbox_light.png"),
        # ---- Cleanup -------------------------------------------------------
        *actions_iterm_window_size(WINDOW_WIDTH, WINDOW_HEIGHT),
        *actions_clear(),
    ]

def scene_configuration():
    return [

        # ********************************************************************
        # **** Configuration *************************************************
        # ********************************************************************

        # ---- Set color scheme ----------------------------------------------
        *actions_colors(DEFAULT_ITERM_COLORS, DEFAULT_PALETTE),
        # ---- Prepare -------------------------------------------------------
        *actions_command_list([
            "git reset --hard HEAD~1 -q",
            "git pull",
            "cd ~",
        ]),
        *actions_clear(),

        # ====================================================================
        # ==== Battery =======================================================
        # ====================================================================
        *actions_command_list([
            "export STARSHIP_COCKPIT_MEMORY_USAGE_ENABLED=true",
        ]),
        *actions_iterm_window_size(WINDOW_WIDTH, WINDOW_HEIGHT_SINGLE),
        *actions_clear(),
        # ---- Make screenshot -----------------------------------------------
        *actions_screenshot("assets/configuration/memory_usage.png"),
        # ---- Cleanup -------------------------------------------------------
        *actions_iterm_window_size(WINDOW_WIDTH, WINDOW_HEIGHT),
        *actions_command_list([
            "export STARSHIP_COCKPIT_MEMORY_USAGE_ENABLED=false",
        ]),
        *actions_clear(),

        # ====================================================================
        # ==== Battery =======================================================
        # ====================================================================
        *actions_command_list([
            "export STARSHIP_COCKPIT_BATTERY_ENABLED=true",
            "export STARSHIP_COCKPIT_BATTERY_THRESHOLD=100",
        ]),
        *actions_iterm_window_size(WINDOW_WIDTH, WINDOW_HEIGHT_SINGLE),
        *actions_clear(),
        # ---- Make screenshot -----------------------------------------------
        *actions_screenshot("assets/configuration/battery.png"),
        # ---- Cleanup -------------------------------------------------------
        *actions_iterm_window_size(WINDOW_WIDTH, WINDOW_HEIGHT),
        *actions_command_list([
            "export STARSHIP_COCKPIT_BATTERY_ENABLED=false",
        ]),
        *actions_clear(),

        # ====================================================================
        # ==== Keyboard Layout ===============================================
        # ====================================================================
        *actions_command_list([
            "export STARSHIP_COCKPIT_KEYBOARD_LAYOUT_ENABLED=true",
            "export STARSHIP_COCKPIT_KEYBOARD_LAYOUT_ABC=ENG",
            "export STARSHIP_COCKPIT_KEYBOARD_LAYOUT_UKRAINIAN=UKR",
        ]),
        *actions_iterm_window_size(WINDOW_WIDTH, WINDOW_HEIGHT_SINGLE),
        *actions_clear(),
        # ---- Make screenshot -----------------------------------------------
        *actions_screenshot("assets/configuration/keyboard_layout.png"),
        # ---- Cleanup -------------------------------------------------------
        *actions_iterm_window_size(WINDOW_WIDTH, WINDOW_HEIGHT),
        *actions_command_list([
            "export STARSHIP_COCKPIT_KEYBOARD_LAYOUT_ENABLED=false",
        ]),
        *actions_clear(),
    ]

def scene_cleanup():
    return [

        # ********************************************************************
        # **** Cleanup *******************************************************
        # ********************************************************************

        # ---- Set color scheme ----------------------------------------------
        *actions_colors(DEFAULT_ITERM_COLORS, DEFAULT_PALETTE),
        # ---- Cleanup -------------------------------------------------------
        *actions_command_list([
            f"cd {os.getcwd()}",
            "rm -rf starship-cockpit-demo",
        ]),
        # ---- Close iTerm ---------------------------------------------------
        *actions_iterm_close(),
    ]

def actions_colors(iterm_colors_name, palette_name):
    return [
        {
            "type": "command",
            "command": r"echo -e '\033]50;SetProfile=" + iterm_colors_name + r"\007'",
            "delay_after": 1/2,
        },
        {
            "type": "set_palette",
            "palette": palette_name,
            "delay_after": 1,
        },
        {
            "type": "command",
            "command": r"echo -e '\033]0;Starship Cockpit Demo\007'",
            "delay_after": 1/2,
        },
    ]

def actions_clear():
    return [
        {
            "type": "command",
            "command": "clear",
            "delay_after": 1/2,
        }
    ]

def actions_iterm_window_size(width, height):
    return [
        {
            "type": "set_iterm_window_size",
            "width": width,
            "height": height,
            "delay_after": 1/2,
        },
    ]

def actions_screenshot(filepath):
    return [
        {
            "type": "screenshot",
            "filepath": filepath,
            "delay_before": 2,
            "delay_after": 1/2,
        },
    ]

def actions_iterm_open():
    return [
        {
            "type": "open_iterm",
            "delay_after": 5,
        },
    ]

def actions_iterm_close():
    return [
        {
            "type": "close_iterm",
            "delay_after": 2,
        },
    ]

def actions_command_list(commands, command_delay=1/2, delay_after=1/2, delay_before=0):
    return [
        {
            "type": "command_list",
            "commands": commands,
            "command_delay": command_delay,
            "delay_after": delay_after,
            "delay_before": delay_before,
        },
    ]

def run_applescript(script, action_name="Unknown action"):
    try:
        result = applescript.run(script)
        if result.err:
            print(f"AppleScript Error in {action_name}: {result.err}")
            return None
        return result
    except Exception as e:
        print(f"Failed to execute {action_name}: {e}")
        return None

def format_action_details(action):
    return ' '.join(f'{k}="{v}"' for k, v in action.items())

def escape_command(command):
    command = command.replace('\\', '\\\\')
    return command

def process_actions(*actions):
    for action in actions:
        print(f"Running action: {format_action_details(action)}")
        
        delay_before = action.get("delay_before", 0)
        delay_after = action.get("delay_after", 0)

        time.sleep(delay_before)

        if action["type"] == "open_iterm":
            script = '''
            tell application "iTerm2"
                create window with default profile
            end tell
            '''
            run_applescript(script, "open_iterm")

        elif action["type"] == "set_iterm_window_size":
            script = f"""
            tell application "iTerm2"
                tell current window
                    set bounds to {{0, 0, {action["width"]}, {action["height"]}}}
                end tell
            end tell
            """
            run_applescript(script, "set_iterm_window_size")

        elif action["type"] == "command":
            escaped_command = escape_command(action['command'])
            cmd_script = f"""
            tell application "iTerm2"
                tell current window
                    tell current session
                        write text "{escaped_command}"
                    end tell
                end tell
            end tell
            """
            run_applescript(cmd_script, f"command: {action['command']}")

        elif action["type"] == "command_list":
            for cmd in action["commands"]:
                escaped_command = escape_command(cmd)
                cmd_script = f"""
                tell application "iTerm2"
                    tell current window
                        tell current session
                            write text "{escaped_command}"
                        end tell
                    end tell
                end tell
                """
                run_applescript(cmd_script, f"command: {cmd}")
                time.sleep(action.get("command_delay", 0.5))  # Optional delay between commands

        elif action["type"] == "screenshot":
            bounds_script = """
            tell application "iTerm2"
                get bounds of window 1
            end tell
            """
            bounds = run_applescript(bounds_script, "get_bounds")
            if bounds:
                x, y, width, height = bounds.out.strip("{}").split(",")
                x, y, width, height = map(int, [x, y, width, height])

                screenshot = ImageGrab.grab(bbox=(x, y, width, height))
                screenshot.save(action["filepath"])

        elif action["type"] == "set_palette":
            palette_name = action["palette"]
            starship_config = "starship.toml"
            
            with open(starship_config, 'r') as file:
                content = file.readlines()
            
            for i, line in enumerate(content):
                if line.startswith("palette = "):
                    content[i] = f"palette = '{palette_name}'\n"
                    break
            
            with open(starship_config, 'w') as file:
                file.writelines(content)

        elif action["type"] == "close_iterm":
            script = """
            tell application "iTerm2"
                close window 1
            end tell
            """
            run_applescript(script, "close_iterm")

        time.sleep(delay_after)

def run_actions():
    try:
        process_actions(
            *scene_init(),
            *scene_demo(),
            *scene_palettes(),
            *scene_configuration(),
            *scene_cleanup()
        )
    except KeyboardInterrupt:
        print("\n\nScript interrupted by user. Cleaning up...\n")
        # Ignore ALL keyboard interrupts during cleanup
        original_handler = signal.signal(signal.SIGINT, signal.SIG_IGN)
        try:
            process_actions(
                *scene_cleanup(),
            )
        finally:
            # Restore original interrupt handler
            signal.signal(signal.SIGINT, original_handler)


if __name__ == "__main__":
    run_actions()
