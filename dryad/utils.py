import subprocess
from typing import Any, Callable, Union, List

from . import container as DryadContainer
from .common import DryadEnv, DryadFlag


def run_shell_cmd(cmd: str) -> None:
    assert isinstance(
        cmd, str
    ), f'[Dryad.DryadUtil::run_shell_cmd] cmd arg is "{cmd}", that is not a str var.'
    if DryadEnv.OSTYPE == "win32":
        subprocess.run(["powershell", "-Command", cmd], check=True)
    elif DryadEnv.OSTYPE == "linux" or DryadEnv.OSTYPE == "darwin":
        subprocess.run(["bash", "-c", cmd], check=True)
    else:
        assert (
            False
        ), f"[Dryad.DryadUtil::run_shell_cmd] The OS {DryadEnv.OSTYPE} is not supported."


ErrStopCmd: str = ""  # need config
PrefixCmds: List[str] = []
DryadFlags: List[DryadFlag] = []


if DryadEnv.OSTYPE == "win32":
    ErrStopCmd = '$ErrorActionPreference = "Stop"'
elif DryadEnv.OSTYPE == "linux" or DryadEnv.OSTYPE == "darwin":
    ErrStopCmd = "set -e"
else:
    assert False, DryadEnv.OSTYPE + " not supported."


def flag_push(flag: DryadFlag, data: Union[str, list, None] = None):
    if flag == DryadFlag.PrefixCmd:
        if type(data) is str:
            PrefixCmds.append(data)
        elif type(data) is list:
            PrefixCmds.extend(data)
        else:
            assert False
    elif (
        flag == DryadFlag.InVisible
        or flag == DryadFlag.IgnoreErr
        or flag == DryadFlag.Anchoring
    ):
        DryadFlags.append(flag)
    elif flag == DryadFlag.AcceptArg:
        if DryadContainer.DryadArg is None:
            print("\033[31m" + "No DryadArg provided." + "\033[0m")
            exit(-1)
    else:
        assert False


def flag_pop(flag: DryadFlag, data: Union[str, list, None] = None):
    assert type(flag) is DryadFlag
    if flag == DryadFlag.PrefixCmd:
        if type(data) is str:
            PrefixCmds.pop()
        elif type(data) is list:
            for _ in range(len(data)):
                PrefixCmds.pop()
        else:
            assert False
    elif (
        flag == DryadFlag.InVisible
        or flag == DryadFlag.IgnoreErr
        or flag == DryadFlag.Anchoring
    ):
        DryadFlags.pop()
    elif flag == DryadFlag.AcceptArg:
        pass
    else:
        assert False


def dryad_run_shell_cmd(cmd: str) -> None:
    assert len(ErrStopCmd) > 0
    pre_cmd = PrefixCmds

    if DryadFlag.Anchoring not in DryadFlags:
        pre_cmd = [f"cd {DryadEnv.SCRIPTPATH}"] + pre_cmd

    if DryadFlag.IgnoreErr not in DryadFlags:
        pre_cmd = [ErrStopCmd] + pre_cmd

    # set -> cd main_path -> pre cmd -> cmd

    if DryadFlag.InVisible not in DryadFlags:
        print("\033[33;1m" + cmd + "\033[0m")

    cmd = "\n".join(pre_cmd) + "\n" + cmd

    try:
        run_shell_cmd(cmd)
    except subprocess.CalledProcessError as e:
        if DryadFlag.IgnoreErr not in DryadFlags:
            if DryadFlag.InVisible not in DryadFlags:
                print("\033[41m\033[37m" + "Fail" + "\033[0m")
            exit(-1)
    except Exception as e:
        assert False
    # print("\033[42m\033[37m" + "Pass" + "\033[0m")


def strip_line(text: str) -> str:
    """去除首尾空行"""
    while len(text) > 0 and text[0] == "\n":
        text = text[1:]
    while len(text) > 0 and text[-1] == "\n":
        text = text[:-1]
    return text


def left_shift(text: str) -> str:
    """去除文本左空列"""
    if len(text) == 0:
        return text

    lines = text.split("\n")

    def get_prefix_space_num(s: str) -> int:
        assert "\n" not in s, "only support a line."
        for i, c in enumerate(s):
            if c != " ":
                return i
        return len(s)

    max_prefix_space_num: int = min(
        [get_prefix_space_num(line) for line in lines if len(line.strip()) != 0]
    )
    lines = [
        line[max_prefix_space_num:] if len(line.strip()) != 0 else line
        for line in lines
    ]
    return "\n".join(lines)


def right_shift(text: str, dist: int) -> str:
    """整个文本右移(在左边填充空列对齐)"""
    lines = text.split("\n")
    for i in range(len(lines)):
        lines[i] = (" " * dist) + lines[i]
    return "\n".join(lines)


def dryad_shift(text: str, dist: int, first: bool) -> str:
    """
    消除左边空列,
    然后右对齐,
        如果是文本的第一部分, 则其第一行不右移动,
        否则全部右移
    """
    text = strip_line(text)
    text = left_shift(text)
    if first is False:
        return right_shift(text, dist)
    if len(text.split("\n")) == 1:
        return text
    first_line, text = text.split("\n", maxsplit=1)
    return first_line + "\n" + right_shift(left_shift(text), dist)


def help_opt_func_gen(cmd_tree: dict, prefix_cmds: list):
    DryadTreeLeafNodeType = Union[
        str, Callable, DryadFlag, List[Union[str, Callable, DryadFlag]]
    ]

    def lead_node_to_doc(node_content: DryadTreeLeafNodeType) -> list:
        if type(node_content) is str:
            return [left_shift(node_content.rstrip())]
        elif callable(node_content):
            return [left_shift(str(node_content.__doc__).rstrip())]
        elif type(node_content) is DryadFlag:
            return [str(node_content)]
        elif type(node_content) is list:
            return [
                ele for content in node_content for ele in lead_node_to_doc(content)
            ]
        else:
            assert False

    def dfs_internal_node(node: Union[dict, DryadTreeLeafNodeType], prefix_opts: list):
        if type(node) is not dict:
            prefix_opt = " ".join(prefix_opts)
            prefix_len = len(prefix_opt + ": ")
            assert not isinstance(node, dict)  # for mypy, it's only know isinstance
            parts = lead_node_to_doc(node)

            print(f"\033[36m{prefix_opt}\033[0m: ", end="")
            for i, part in enumerate(parts):
                line = dryad_shift(part, prefix_len, True if i == 0 else False)
                if i % 2 == 0:
                    print(f"\033[33m{line}\033[0m")
                else:
                    print(f"\033[32m{line}\033[0m")
            return
        for opt, son_node in node.items():
            if type(opt) is tuple:
                prefix_cmds.append("/".join(opt))
            elif type(opt) is str:
                prefix_cmds.append(opt)
            elif type(opt) is DryadFlag:
                prefix_cmds.append(str(opt))
            else:
                assert False
            dfs_internal_node(son_node, prefix_cmds)
            prefix_cmds.pop()

    def func_gen():
        """Print commands and desciptions supported by script.py."""
        print("该脚本命令可分为两大类")
        print("  Shell Commands, help会输出命令本身")
        print("  Python Function, help会输出函数的__doc__")

        dfs_internal_node(cmd_tree, prefix_cmds)

    return func_gen


def help_opt_cmd_tree_gen(cmd_tree: dict, prefix_cmds: list) -> dict:
    cmd_tree[("-h", "--help")] = help_opt_func_gen(cmd_tree, prefix_cmds)
    # help_opt_func_gen返回的是一个可调用的函数, 但是这里还没有调用, 只有在真正调用时才遍历树, 所以合法
    return cmd_tree


def cmd_tree_match_opt(cmd_tree: dict, opt: str) -> Union[Any, None]:
    for k, v in cmd_tree.items():
        if (type(k) is str and opt == k) or (type(k) is tuple and opt in k):
            return v
    return None
