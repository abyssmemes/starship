# Cockpit preset for [Starship](https://starship.rs/)

This is a preset for the [Starship](https://starship.rs/) cross-shell prompt.

![Starship Cockpit Demo](./assets/images/demo.png)

## Requirements

Install and enable a [Nerd Font](https://www.nerdfonts.com/) in your terminal.

Install [Starship](https://starship.rs/) and configure your shell to use it.

> [!TIP]
> More information about Starship installation and configuration can be found [here](https://starship.rs/guide/#%F0%9F%9A%80-installation).

## Installation

Copy the [`starship.toml`](./starship.toml) file to your Starship configuration directory.

> [!TIP]
> More information about Starship configuration files can be found [here](https://starship.rs/config/#configuration).

## Palettes

This preset includes predefined palettes that you can enable by setting the `palette` value in your `starship.toml` file.

> [!NOTE]
> Background color is not included in the palette. You can set it in your terminal settings.

### Default

![Starship Cockpit Default Palette](./assets/images/palettes/default.png)

```toml
palette = "default"
```

> [!IMPORTANT]
> The default palette uses standard terminal colors, ensuring it blends with your terminal color scheme. In the image you can see the [Tokyo Night](https://raw.githubusercontent.com/mbadolato/iTerm2-Color-Schemes/master/schemes/tokyonight.itermcolors) iTerm2 color scheme.

### Gruvbox Dark

![Starship Cockpit Gruvbox Dark Palette](./assets/images/palettes/gruvbox_dark.png)

```toml
palette = "gruvbox_dark"
```

### Gruvbox Light

![Starship Cockpit Gruvbox Light Palette](./assets/images/palettes/gruvbox_light.png)

```toml
palette = "gruvbox_light"
```

## Configuration

Environment variables can be set in your shell's configuration file:
- Bash: `~/.bashrc`
- Zsh: `~/.zshrc`
- Fish: `~/.config/fish/config.fish`
- PowerShell: PowerShell profile

Remember to restart your shell after setting environment variables.

### Memory Usage

![Starship Cockpit Memory Usage](./assets/images/configuration/memory_usage.png)

Environment variables:

| Variable | Default | Possible values | Description  |
| -------- | ------- | --------------- | ------------ |
| `STARSHIP_COCKPIT_MEMORY_USAGE_ENABLED` | `false` | `true`, `false` | Enable or disable the memory usage module. |

Example configuration:
```bash
export STARSHIP_COCKPIT_MEMORY_USAGE_ENABLED=true
```

### Battery

![Starship Cockpit Battery](./assets/images/configuration/battery.png)

Environment variables:

| Variable | Default | Possible values | Description  |
| -------- | ------- | --------------- | ------------ |
| `STARSHIP_COCKPIT_BATTERY_ENABLED` | `false` | `true`, `false` | Enable or disable the battery module. |
| `STARSHIP_COCKPIT_BATTERY_THRESHOLD` | `100` | `0` - `100` | Set the battery threshold in percentage when the battery info will start to be shown. |

Example configuration:
```bash
export STARSHIP_COCKPIT_BATTERY_ENABLED=true
export STARSHIP_COCKPIT_BATTERY_THRESHOLD=10
```

### Keyboard Layout

![Starship Cockpit Keyboard Layout](./assets/images/configuration/keyboard_layout.png)

> [!NOTE]
> Currently, the keyboard layout module is only supported on macOS. Support for other operating systems may be added in the future.

Environment variables:

| Variable | Default | Possible values | Description  |
| -------- | ------- | --------------- | ------------ |
| `STARSHIP_COCKPIT_KEYBOARD_LAYOUT_ENABLED` | `false` | `true`, `false` | Enable or disable the keyboard layout module. |
| `STARSHIP_COCKPIT_KEYBOARD_LAYOUT_[LAYOUT_ID]` | - | - | Custom alias for layout. |

Example configuration:
```bash
export STARSHIP_COCKPIT_KEYBOARD_LAYOUT_ENABLED=true
export STARSHIP_COCKPIT_KEYBOARD_LAYOUT_ABC=ENG
export STARSHIP_COCKPIT_KEYBOARD_LAYOUT_UKRAINIAN=UKR
```
