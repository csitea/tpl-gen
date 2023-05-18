import os
import time
from rich.console import Console

console = Console(width=150, color_system="truecolor")
err_console = Console(width=150, stderr=True, color_system="truecolor")


def stamp_time(msg):
    ts = time.strftime("%Y-%m-%d %H:%M:%S %Z")
    return f"{ts} ::: {msg}"


def print_warn(msg):
    console.print(f":warning: ::: {msg}", style="light_goldenrod1")


def print_error(msg):
    console.print(f":x: ::: {msg}", style="deep_pink2")


def print_success(msg):
    console.print(f"{msg} ::: :white_heavy_check_mark:", style="green_yellow")


def print_info(msg):
    console.print(f"{msg}", style="light_steel_blue1")


def force_error(err_msg):
    msg = f":fire: ::: {err_msg}"
    err_console.print(msg, style="underline blink red3")
    raise Exception(msg)


def get_required_env_var(var_name):
    env_var = os.getenv(var_name)
    if env_var is None:
        force_error(f"The environment variable \"{var_name}\" does not have a value!\n" +
                    f"In the calling shell do \"export {var_name}=your-{var_name}-value\"")
    return env_var

def get_optional_env_var(var_name):
    env_var = os.getenv(var_name)
    if env_var is None:
        print_warn(f"The environment variable \"{var_name}\" does not have a value!\n" +
                    f"In the calling shell do \"export {var_name}=your-{var_name}-value\"")
    return env_var
