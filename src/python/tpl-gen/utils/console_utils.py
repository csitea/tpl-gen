import time
import yaml
from rich.console import Console

console = Console(width=150, color_system="truecolor")
err_console = Console(width=150, stderr=True, color_system="truecolor")


def stamp_time(msg: str):
    """Prepend the current timestamp to the provided message."""
    ts = time.strftime("%Y-%m-%d %H:%M:%S %Z")
    return f"{ts} ::: {msg}"


def print_warn(msg: str):
    """Print a warning message to the console with specific styling and warning icon."""
    console.print(f"WARN ::: {msg} ::: :warning:", style="light_goldenrod1")


def print_error(msg: str):
    """Print an error message to the console with specific styling and error icon."""
    console.print(f"ERROR ::: {msg} ::: :x:", style="deep_pink2")


def print_success(msg: str):
    """Print a success message to the console with specific styling and check mark icon."""
    console.print(
        f"SUCCESS ::: {msg} ::: :white_heavy_check_mark:", style="green_yellow"
    )


def print_info(msg: str):
    """Print an informational message to the console with specific styling."""
    console.print(f"INFO ::: {msg}", style="light_steel_blue1")


def print_info_heading(heading: str):
    console.rule(heading, style="light_steel_blue1")


def pretty_print_yaml(data):
    """Print a Python data structure to the console in a YAML-formatted way."""
    print(yaml.dump(data, default_flow_style=False, sort_keys=False))
