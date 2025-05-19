# generate help function for cmd tree dict

import textwrap
from typing import Callable, List

from .common import (
    DryadsCmdTreeInternalNodeKeyType,
    DryadsCmdTreeLeafNodeType,
    DryadsCmdTreeNodeType,
    DryadsFlag,
)


def _left_shift(text: str) -> str:
    """Remove the left empty column of the text, keep the empty line`

    Args:
        text: input text

    Returns:
        text after removing the left empty column, keep the original line structure
    """
    if text is None or len(text) == 0:
        return text
    return textwrap.dedent(text)


def _right_shift(text: str, dist: int) -> str:
    """Shift the text to the right by a specified distance.

    Args:
        text: the text to process
        dist: the distance to shift (number of spaces)

    Returns:
        processed text string

    Raises:
        ValueError: when dist is negative
    """
    if dist < 0:
        raise ValueError("dist can't be negative")

    if text is None or len(text) == 0:
        return text

    # textwrap.indent(text, " " * dist)
    return "\n".join(" " * dist + line for line in text.split("\n"))


def _doc_std(text: str) -> List[str]:
    """_summary_

    1. left align
    2. remove start endl
    3. remove end space
    4. split by endl

    Args:
        text (str): _description_

    Returns:
        List[str]: _description_
    """
    return _left_shift(text).lstrip("\n").rstrip().split("\n")


def _leaf_to_doc(leaf: DryadsCmdTreeLeafNodeType) -> List[str]:
    if isinstance(leaf, str):
        return [*_doc_std(leaf)]
    elif callable(leaf):
        return [*_doc_std(leaf.__doc__ if leaf.__doc__ is not None else leaf.__name__)]
    elif isinstance(leaf, DryadsFlag):
        return [str(leaf)]
    elif isinstance(leaf, list):
        return [row for ele in leaf for row in _leaf_to_doc(ele)]
    else:
        assert False


def _internal_key_to_sub_cmd(internal_key: DryadsCmdTreeInternalNodeKeyType) -> str:
    if isinstance(internal_key, str):
        return internal_key
    elif isinstance(internal_key, DryadsFlag):
        return str(internal_key)
    elif isinstance(internal_key, tuple):
        return "/".join(internal_key)
    else:
        assert False


def _sub_cmds_dye(text: str) -> str:
    return f"\033[36m{text}\033[0m"


def _sub_cmds_print(sub_cmds: List[str]) -> int:
    """_summary_

    Args:
        sub_cmds (List[str]): _description_

    Returns:
        int: print char len

    Examples:
        >>> _sub_cmds_print(["ls", "-l"])
        ls -l5
        >>> _sub_cmds_print(["ls", "-l", "-a"])
        ls -l -a8
    """
    text = " ".join(sub_cmds)
    print(_sub_cmds_dye(text), end="")
    return len(text)


def _doc_dye_gen() -> Callable:
    idx = 0

    def dye_func(text: str) -> str:
        nonlocal idx
        idx += 1
        if idx % 2 == 0:
            return f"\033[33m{text}\033[0m"
        else:
            return f"\033[32m{text}\033[0m"

    return dye_func


def _doc_print(doc: List[str], align_len: int) -> None:
    dye_func = _doc_dye_gen()
    for idx, line in enumerate(doc):
        if idx != 0:  # 不是第一个
            line = _right_shift(line, align_len)
        line = dye_func(line)
        print(line, end="")
        if idx != len(doc) - 1:  # 不是最后一个
            print()


def _help_cmd_func(cmd_node: DryadsCmdTreeNodeType, pre_sub_cmd: List[str]) -> None:
    """
    dfs cmd tree, store path;
    if leaf node, print path and doc for leaf.

    Args:
        cmd_node (DryadsCmdTree): dfs node
        pre_sub_cmd (List[str]): dfs pre path
    """
    if not isinstance(cmd_node, dict):  # leaf node, print doc
        align_len = _sub_cmds_print(pre_sub_cmd)
        print(": ", end="")
        _doc_print(_leaf_to_doc(cmd_node), align_len + 2)
        print()
        return

    assert isinstance(cmd_node, dict)  # Defensive programming
    for k, v in cmd_node.items():  # dfs
        pre_sub_cmd.append(_internal_key_to_sub_cmd(k))
        _help_cmd_func(v, pre_sub_cmd)
        pre_sub_cmd.pop()


def gen_help_cmd_func(cmd_tree: DryadsCmdTreeNodeType) -> Callable:
    def help_cmd_func_template():
        """Print commands and desciptions supported by script.py."""
        print("该脚本命令可分为两大类")
        print("  Shell Commands, help会输出命令本身")
        print("  Python Function, help会输出函数的__doc__")

        _help_cmd_func(cmd_tree, [])

    return help_cmd_func_template
