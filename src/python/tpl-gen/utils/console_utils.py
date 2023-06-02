import time
import yaml
from rich.console import Console

console = Console(width=150, color_system="truecolor")
err_console = Console(width=150, stderr=True, color_system="truecolor")


def stamp_time(msg):
    ts = time.strftime("%Y-%m-%d %H:%M:%S %Z")
    return f"{ts} ::: {msg}"


def print_warn(msg):
    console.print(f"WARN ::: {msg} ::: :warning:", style="light_goldenrod1")


def print_error(msg):
    console.print(f"ERROR ::: {msg} ::: :x:", style="deep_pink2")


def print_success(msg: str):
    console.print(
        f"SUCCESS ::: {msg} ::: :white_heavy_check_mark:", style="green_yellow"
    )


def print_info(msg):
    console.print(f"INFO ::: {msg}", style="light_steel_blue1")


def pretty_print_yaml(data):
    print(yaml.dump(data, default_flow_style=False, sort_keys=False))
