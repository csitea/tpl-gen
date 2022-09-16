import os
import time
from colorama import Fore, Style



def stamp_time(msg):
    ts = time.strftime("%Y-%m-%d %H:%M:%S %Z")
    return f"{ts} ::: {msg}"


def print_warn(msg):
    msg = stamp_time(msg)
    print(f"{Fore.YELLOW}{msg}{Style.RESET_ALL}")


def print_error(msg):
    msg = stamp_time(msg)
    print(f"{Fore.RED}{msg}{Style.RESET_ALL}")


def print_success(msg):
    msg = stamp_time(msg)
    print(f"{Fore.GREEN}{msg}{Style.RESET_ALL}")


def print_info(msg):
    msg = stamp_time(msg)
    print(f"{Fore.BLUE}{msg}{Style.RESET_ALL}")


def force_error(err_msg):
    msg = stamp_time(err_msg)
    msg = f"[FATAL] ::: {err_msg}"
    print_error(msg)
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
