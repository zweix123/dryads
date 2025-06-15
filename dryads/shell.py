import subprocess
import sys

from .common import DryadsFlag, env, flag_stack


def run_shell_cmd(cmd: str) -> None:
    assert isinstance(
        cmd, str
    ), f'[dryads.run_shell_cmd] cmd arg is "{cmd}", that is not a str var.'
    if sys.platform == "win32":
        subprocess.run(["powershell", "-Command", cmd], check=True)
    elif sys.platform == "linux" or sys.platform == "darwin":
        subprocess.run(["bash", "-c", cmd], check=True)
    else:
        assert False, f"[dryads.run_shell_cmd] The OS {sys.platform} is not supported."


shell_err_stop_cmd: str = str()


def dryads_run_shell_cmd(cmd: str) -> None:
    global shell_err_stop_cmd
    if len(shell_err_stop_cmd) == 0:
        if sys.platform == "win32":
            shell_err_stop_cmd = '$ErrorActionPreference = "Stop"'
        elif sys.platform == "linux" or sys.platform == "darwin":
            shell_err_stop_cmd = "set -e"
        else:
            assert False, sys.platform + " not supported."

    pre_cmds = flag_stack.get_prefix_cmds()

    if not flag_stack.contains(DryadsFlag.Anchoring):
        pre_cmds = [f"cd {env.script_path}"] + pre_cmds

    if not flag_stack.contains(DryadsFlag.InVisible):
        print("\033[33;1m" + cmd + "\033[0m")
        sys.stdout.flush()

    if not flag_stack.contains(DryadsFlag.IgnoreErr):
        pre_cmds = [shell_err_stop_cmd] + pre_cmds

    cmd = "\n".join(pre_cmds) + "\n" + cmd

    try:
        run_shell_cmd(cmd)
    except subprocess.CalledProcessError as e:
        if not flag_stack.contains(DryadsFlag.IgnoreErr):
            if not flag_stack.contains(DryadsFlag.InVisible):
                print("\033[41m\033[37m" + "Fail" + "\033[0m")
                sys.stdout.flush()
            exit(-1)
    except Exception as e:
        assert False, e
