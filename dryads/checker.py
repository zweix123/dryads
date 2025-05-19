# check the cmd tree dict structure

from typing import Callable, List, Tuple, Union

from .common import (
    DryadsCmdTreeInternalNodeType,
    DryadsCmdTreeLeafNodeType,
    DryadsCmdTreeNodeType,
    DryadsFlag,
)


def _check_sub_cmd(sub_cmd: str) -> None:
    if not isinstance(sub_cmd, str):
        raise Exception("[dryads.check] The sub command must be a str.")
    if len(sub_cmd) == 0:
        raise Exception("[dryads.check] The sub command must be a non-empty str.")
    if " " in sub_cmd:
        raise Exception("[dryads.check] The sub command must not contain space.")


def _check_multi_choice_sub_cmd(opt_sub_cmd: Tuple[str, ...]) -> None:
    # if input tuple is single value, etc, (3.14), (42), ("s")
    if not isinstance(opt_sub_cmd, tuple):
        raise Exception("[dryads.check] The optional sub command must be a tuple.")

    if len(opt_sub_cmd) == 0:
        raise Exception(
            "[dryads.check] The optional sub command must be a non-empty tuple."
        )
    if not all(isinstance(ele, str) for ele in opt_sub_cmd):
        raise Exception(
            "[dryads.check] The optional sub command must be a tuple of str."
        )
    if len(opt_sub_cmd) != len(set(opt_sub_cmd)):
        raise Exception(
            "[dryads.check] The optional sub command must be a tuple of unique str."
        )
    for sub_cmd in opt_sub_cmd:
        _check_sub_cmd(sub_cmd)


def _check_dryads_flag_internal(flag: DryadsFlag) -> None:
    # Currently, only this key is quite unique
    if flag != DryadsFlag.PrefixCmd:
        raise Exception(
            "[dryads.check] The dryads flag in internal node must be DryadsFlag.PrefixCmd."
        )


def _check_dryads_flag_leaf(flag: DryadsFlag) -> None:
    # Currently, only this key is quite unique
    if flag == DryadsFlag.PrefixCmd:
        raise Exception(
            "[dryads.check] The dryads flag in leaf node must not be DryadsFlag.PrefixCmd."
        )


def _check_shell_cmd(shell_cmd: str) -> None:
    # nothing
    pass


def _check_func(func: Callable) -> None:
    # nothing
    pass


def _check_cmd_tree_leaf(leaf: DryadsCmdTreeLeafNodeType) -> None:
    type_exception = Exception(
        "[dryads.check] The command tree leaf node must be str, Callable, DryadsFlag or list of them."
    )
    if isinstance(leaf, str):
        _check_shell_cmd(leaf)
    elif callable(leaf):
        _check_func(leaf)
    elif isinstance(leaf, DryadsFlag):
        # The inclusion of DryadFlag in DryadCMDTreeLeafNodeType type
        # is to ensure the completeness of the type system,
        # and in fact, there should not be a separate DryadFlag as a leaf.
        assert False
    elif isinstance(leaf, list):
        for ele in leaf:
            if isinstance(ele, str):
                _check_shell_cmd(ele)
            elif callable(ele):
                _check_func(ele)
            elif isinstance(ele, DryadsFlag):
                _check_dryads_flag_leaf(ele)
            else:
                raise type_exception
    else:
        # Although type analysis suggests that it will not enter this branch,
        # Python is dynamically typed and type analysis is incremental,
        # so users can still pass in parameters that do not meet the requirements.
        raise type_exception


def _check_cmd_tree_internal(node: DryadsCmdTreeInternalNodeType) -> None:
    # Because it supports optional sub command through tuple,
    # it is not possible to directly get all keys through dict.keys()
    # but rather to manually process each key
    assert isinstance(node, dict)  # for mypy
    keys: List[Union[str, DryadsFlag]] = []
    for key in node.keys():
        if isinstance(key, str):  # sub command
            _check_sub_cmd(key)
            keys.append(key)
        elif isinstance(key, DryadsFlag):  # dryads flag
            _check_dryads_flag_internal(key)
            keys.append(key)
        elif isinstance(key, tuple):  # multiple choice sub command
            _check_multi_choice_sub_cmd(key)
            keys.extend(key)
        else:
            raise Exception(
                "[dryads.check] The command tree internal node keys only support str, DryadsFlag or tuple[str]."
            )
    if len(keys) != len(set(keys)):
        raise Exception("[dryads.check] sub command conflicts.")
        # TODO(zweix): More detailed error reporting

    for son in node.values():
        check_cmd_tree(son)


def check_cmd_tree(node: DryadsCmdTreeNodeType) -> None:
    if isinstance(node, dict):  # internal node
        _check_cmd_tree_internal(node)
    else:  # leaf node
        _check_cmd_tree_leaf(node)
