import inspect
import os
import sys
from typing import Any, Callable

from . import container as DryadContainer
from . import utils as DryadUtil
from .common import DryadEnv, DryadFlag


class Dryad:
    def __init__(self, cmd_tree: dict) -> None:
        DryadEnv.SCRIPTPATH = os.path.dirname(inspect.stack()[1].filename)  # trick

        self.cmd_tree = cmd_tree
        self.opts: list[str] = []

        self.check()
        self.config()
        self.main()

    def check(self) -> None:
        """
        + internal node: dict, key is str | tuple[str] | DryadFlag
        + leaf node: DryadFlag, str, Callable, list[DryadFlag | str | Callable]
        """

        def check_cmd_tree(
            cmd_tree_node: dict | list | str | Callable | DryadFlag,
        ) -> None:
            if type(cmd_tree_node) == dict:
                # internal node
                opts = [
                    opt
                    for key in cmd_tree_node.keys()
                    for opt in (key if type(key) == list else [key])
                ]
                if len(opts) != len(set(opts)):
                    raise Exception("[Drayd] Conflicting opts in commands dict.")
                for son_node in cmd_tree_node.values():
                    check_cmd_tree(son_node)
            else:
                # leaf node
                if type(cmd_tree_node) == list:
                    if any([type(ele) == dict for ele in cmd_tree_node]):
                        raise Exception(
                            "[Drayd] There are alse dict ele in the leaf nodes of cmd dict."
                        )
                elif type(cmd_tree_node) == DryadFlag:
                    raise Exception("[Drayd] DryadFlag should not be used alone.")

        check_cmd_tree(self.cmd_tree)

    def config(self) -> None:
        # add command 'env'
        if DryadUtil.cmd_tree_match_opt(self.cmd_tree, "env") is not None:
            raise Exception("[Dryad] The 'env' option conflicts with built-in opts.")
        self.cmd_tree["env"] = DryadEnv.println

    def main(self) -> None:
        self.opts = sys.argv[1:]
        if len(self.opts) == 0:
            DryadUtil.help_opt_func_gen(self.cmd_tree, [])()
        else:
            self.opt_dfs(self.opts, self.cmd_tree)

    def dfs_run(self, cmds: dict | list | str | Callable):
        if callable(cmds):
            cmds()
        elif type(cmds) is str:
            DryadUtil.dryad_run_shell_cmd(cmds)
        elif type(cmds) is list:
            [DryadUtil.flag_push(ele) for ele in cmds if type(ele) is DryadFlag]
            [self.dfs_run(ele) for ele in cmds if type(ele) is not DryadFlag]
            [DryadUtil.flag_pop(ele) for ele in cmds if type(ele) is DryadFlag]
        elif type(cmds) is dict:
            [DryadUtil.flag_push(k, v) for k, v in cmds.items() if type(k) is DryadFlag]
            [self.dfs_run(v) for k, v in cmds.items() if type(k) is not DryadFlag]
            [DryadUtil.flag_pop(k, v) for k, v in cmds.items() if type(k) is DryadFlag]
        else:
            assert False, cmds

    def opt_dfs(self, opts: list[str], cmds: dict | Any, path: list[str] = []):
        if len(opts) == 0:
            # 通过这个入口执行说明没有AcceptArg, 但执行是递归的, 如果子树有AcceptArg呢?
            def check_subtree_not_accept_arg_flag(cmd_tree_node: dict):
                if type(cmd_tree_node) is dict:
                    # internal node
                    for son_node in cmd_tree_node.values():
                        check_subtree_not_accept_arg_flag(son_node)
                else:
                    # leaf node
                    if type(cmd_tree_node) == list and any(
                        [ele == DryadFlag.AcceptArg for ele in cmd_tree_node]
                    ):
                        print(
                            "\033[31m" + "No DryadArg provided in subtree." + "\033[0m"
                        )
                        exit(-1)

            check_subtree_not_accept_arg_flag(cmds)
            self.dfs_run(cmds)
            return

        if (
            type(cmds) is not dict  # 叶子节点
            and len(opts) == 1  # 参数只剩一个
            and type(cmds) is list  # 叶子内容是列表
            and DryadFlag.AcceptArg in cmds  # DryadFlag.AcceptArg在其中
        ):
            DryadContainer.DryadArg = opts[0]
            self.dfs_run(cmds)
            return

        def internal_match() -> dict | list | str | None:
            dummy = DryadUtil.cmd_tree_match_opt(cmds, opts[0])
            if dummy is not None:
                return dummy

            if opts[0] in ("-h", "--help"):
                return DryadUtil.help_opt_func_gen(cmds, path)

            return None

        if type(cmds) is not dict or internal_match() is None:
            print(f"opts \"{' '.join(self.opts)}\" error", end=", ")
            print(f"unsupported or spelled incorrectly", end=", ")
            print(f'give it a try of option "--help"', end=".\n")
            return

        if DryadFlag.PrefixCmd in cmds:
            DryadUtil.flag_push(DryadFlag.PrefixCmd, cmds[DryadFlag.PrefixCmd])

        self.opt_dfs(opts[1:], internal_match(), path + [opts[0]])

        if DryadFlag.PrefixCmd in cmds:
            DryadUtil.flag_pop(DryadFlag.PrefixCmd, cmds[DryadFlag.PrefixCmd])
