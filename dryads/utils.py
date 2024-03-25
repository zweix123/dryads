import subprocess
from typing import Any, Callable, List, Tuple, Union

from . import container as DryadsContainer
from .common import (
    DryadsCmdTreeInternalType,
    DryadsCmdTreeLeafType,
    DryadsEnv,
    DryadsFlag,
)

# run command ==================================================================


def run_shell_cmd(cmd: str) -> None:
    assert isinstance(
        cmd, str
    ), f'[Dryads.DryadsUtil::run_shell_cmd] cmd arg is "{cmd}", that is not a str var.'
    if DryadsEnv.OSTYPE == "win32":
        subprocess.run(["powershell", "-Command", cmd], check=True)
    elif DryadsEnv.OSTYPE == "linux" or DryadsEnv.OSTYPE == "darwin":
        subprocess.run(["bash", "-c", cmd], check=True)
    else:
        assert (
            False
        ), f"[Dryads.DryadsUtil::run_shell_cmd] The OS {DryadsEnv.OSTYPE} is not supported."


ErrStopCmd: str = ""  # need config
PrefixCmds: List[str] = []
DryadsFlags: List[DryadsFlag] = []


if DryadsEnv.OSTYPE == "win32":
    ErrStopCmd = '$ErrorActionPreference = "Stop"'
elif DryadsEnv.OSTYPE == "linux" or DryadsEnv.OSTYPE == "darwin":
    ErrStopCmd = "set -e"
else:
    assert False, DryadsEnv.OSTYPE + " not supported."


def flag_push(flag: DryadsFlag, data: Union[str, list, None] = None):
    if flag == DryadsFlag.PrefixCmd:
        if type(data) is str:
            PrefixCmds.append(data)
        elif type(data) is list:
            PrefixCmds.extend(data)
        else:
            assert False
    elif (
        flag == DryadsFlag.InVisible
        or flag == DryadsFlag.IgnoreErr
        or flag == DryadsFlag.Anchoring
    ):
        DryadsFlags.append(flag)
    elif flag == DryadsFlag.AcceptArg:
        if DryadsContainer.DryadsArg is None:
            print("\033[31m" + "No DryadsArg provided." + "\033[0m")
            exit(-1)
    else:
        assert False


def flag_pop(flag: DryadsFlag, data: Union[str, list, None] = None):
    assert type(flag) is DryadsFlag
    if flag == DryadsFlag.PrefixCmd:
        if type(data) is str:
            PrefixCmds.pop()
        elif type(data) is list:
            for _ in range(len(data)):
                PrefixCmds.pop()
        else:
            assert False
    elif (
        flag == DryadsFlag.InVisible
        or flag == DryadsFlag.IgnoreErr
        or flag == DryadsFlag.Anchoring
    ):
        DryadsFlags.pop()
    elif flag == DryadsFlag.AcceptArg:
        pass
    else:
        assert False


def dryads_run_shell_cmd(cmd: str) -> None:
    assert len(ErrStopCmd) > 0
    pre_cmd = PrefixCmds

    if DryadsFlag.Anchoring not in DryadsFlags:
        pre_cmd = [f"cd {DryadsEnv.SCRIPTPATH}"] + pre_cmd

    if DryadsFlag.IgnoreErr not in DryadsFlags:
        pre_cmd = [ErrStopCmd] + pre_cmd

    # set -> cd main_path -> pre cmd -> cmd

    if DryadsFlag.InVisible not in DryadsFlags:
        print("\033[33;1m" + cmd + "\033[0m")

    cmd = "\n".join(pre_cmd) + "\n" + cmd

    try:
        run_shell_cmd(cmd)
    except subprocess.CalledProcessError as e:
        if DryadsFlag.IgnoreErr not in DryadsFlags:
            if DryadsFlag.InVisible not in DryadsFlags:
                print("\033[41m\033[37m" + "Fail" + "\033[0m")
            exit(-1)
    except Exception as e:
        assert False
    # print("\033[42m\033[37m" + "Pass" + "\033[0m")


# -h/--help ====================================================================


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


def dryads_shift(text: str, dist: int, first: bool) -> str:
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


def help_opt_func_gen(cmd_tree: dict):
    def lead_node_to_doc(node_content: DryadsCmdTreeLeafType) -> list:
        if type(node_content) is str:
            return [left_shift(node_content.rstrip())]
        elif callable(node_content):
            return [left_shift(str(node_content.__doc__).rstrip())]
        elif type(node_content) is DryadsFlag:
            return [str(node_content)]
        elif type(node_content) is list:
            return [
                ele for content in node_content for ele in lead_node_to_doc(content)
            ]
        else:
            assert False

    last_pre_opts: List[str] = []

    def dfs_internal_node(node: DryadsCmdTreeInternalType, pre_opts: List[str]):
        if type(node) is not dict:
            assert not isinstance(node, dict)  # for mypy, it's only know isinstance
            first = True
            for i in range(len(pre_opts)):
                if first is True:
                    first = False
                else:
                    print(" ", end="")
                if i < len(last_pre_opts) and last_pre_opts[i] == pre_opts[i]:
                    print(pre_opts[i], end="")
                else:
                    print(f"\033[36m{pre_opts[i]}\033[0m", end="")
            last_pre_opts[:] = pre_opts
            print(": ", end="")

            pre_len = (
                sum(list(map(len, pre_opts)))
                + (len(pre_opts) - 1 if len(pre_opts) > 0 else 0)
                + 2
            )

            parts = lead_node_to_doc(node)
            for i, part in enumerate(parts):
                line = dryads_shift(part, pre_len, True if i == 0 else False)
                if i % 2 == 0:
                    print(f"\033[33m{line}\033[0m")
                else:
                    print(f"\033[32m{line}\033[0m")
            return
        for opt, son_node in node.items():
            if type(opt) is tuple:
                pre_opts.append("/".join(opt))
            elif type(opt) is str:
                pre_opts.append(opt)
            elif type(opt) is DryadsFlag:
                pre_opts.append(str(opt))
            else:
                assert False
            dfs_internal_node(son_node, pre_opts)
            pre_opts.pop()

    def func_gen():
        """Print commands and desciptions supported by script.py."""
        print("该脚本命令可分为两大类")
        print("  Shell Commands, help会输出命令本身")
        print("  Python Function, help会输出函数的__doc__")

        dfs_internal_node(cmd_tree, [])

    return func_gen


# command dict check ===========================================================


def _check_cmd_tree_leaf(
    value: Union[
        str,
        Callable,
        List[Union[DryadsFlag, str, Callable, Tuple[DryadsFlag, List[str]]]],
    ]
):
    e = Exception(
        "[Dryads] The commands dict's leaf node must be str, Callable, [DryadsFlag | str | Callable | (DryadsFlag, [str])]"
    )

    def check_cmd_tree_leaf_tuple(value: Tuple[DryadsFlag, List[str]]):
        if not isinstance(value, tuple):
            raise e
        if len(value) != 2:
            raise e
        if not isinstance(value[0], DryadsFlag):
            raise e
        if not isinstance(value[1], list):
            raise e
        if not all(isinstance(ele, str) or callable(ele) for ele in value[1]):
            raise e
        pass

    if isinstance(value, str) or callable(value):
        return
    if isinstance(value, list):
        for ele in value:
            if isinstance(ele, (str, DryadsFlag)) or callable(ele):
                continue
            elif isinstance(ele, tuple):
                check_cmd_tree_leaf_tuple(ele)
            else:
                raise e


def check_cmd_tree(
    cmd_tree_node: Union[dict, list, str, Callable, DryadsFlag],
) -> None:
    internal_exception = Exception(
        "[Dryads] The commands dict's keys only support str, tuple[str] and DryadsFlag."
    )
    if type(cmd_tree_node) == dict:  # internal node
        opts: List[Union[str, DryadsFlag]] = []
        for k in cmd_tree_node.keys():
            if isinstance(k, str):
                opts.append(k)
            elif isinstance(k, tuple):
                if not all(isinstance(ele, str) for ele in k):
                    raise internal_exception
                opts.extend(k)
            elif isinstance(k, DryadsFlag):
                opts.append(k)
            else:
                raise internal_exception
        if any(" " in opt for opt in opts if isinstance(opt, str)):
            raise Exception(
                "[Drayds] There are options have space char in commands dict."
            )
        if len(opts) != len(set(opts)):
            raise Exception("[Drayds] There are conflicting opts in commands dict.")

        for son_node in cmd_tree_node.values():
            check_cmd_tree(son_node)
    else:  # leaf node
        _check_cmd_tree_leaf(cmd_tree_node)


# misc =========================================================================


def cmd_tree_match_opt(cmd_tree: dict, opt: str) -> Union[Any, None]:
    for k, v in cmd_tree.items():
        if (type(k) is str and opt == k) or (type(k) is tuple and opt in k):
            return v
    return None
