import time
import yaml
from rich.console import Console
from rich.pretty import pprint
from rich.abc import RichRenderable

console = Console(width=150, color_system="truecolor")
err_console = Console(width=150, stderr=True, color_system="truecolor")


def stamp_time(msg: str):
    ts = time.strftime("%Y-%m-%d %H:%M:%S %Z")
    return f"{ts} ::: {msg}"


def print_warn(msg: str):
    console.print(f"WARN ::: {msg} ::: [blink2]:warning:", style="light_goldenrod1")


def print_error(msg: str):
    console.print(f"ERROR ::: {msg} ::: :x:", style="deep_pink2")


def print_fatal(msg: str):
    err_console.print(f"FATAL ::: {msg} ::: :skull:", style="bold red")


def print_success(msg: str):
    console.print(
        f"SUCCESS ::: {msg} ::: :white_heavy_check_mark:", style="green_yellow"
    )


def print_yaml(yaml_str: str):
    console.print(yaml_str, style="medium_spring_green")


def print_info(msg: str):
    console.print(f"INFO ::: {msg}", style="medium_spring_green")


def print_renderable(element: RichRenderable):
    console.print(element, style="medium_spring_green")


def print_code(python_obj: any):
    pprint(python_obj, console=console)


def print_info_heading(heading: str):
    console.rule(heading, style="spring_green2")


def pretty_print_yaml(data):
    print(yaml.dump(data, default_flow_style=False, sort_keys=False))
