import inspect
import os
import sys
from typing import Any, Callable, List, Union

from . import container as DryadsContainer
from . import utils as DryadsUtil
from .common import DryadsEnv, DryadsFlag


class Dryads:
    def __init__(self, cmd_tree: dict) -> None:
        DryadsEnv.SCRIPTPATH = os.path.dirname(inspect.stack()[1].filename)  # trick

        self.cmd_tree = cmd_tree
        self.opts: List[str] = []

        self.config()
        self.check()
        self.main()

    def check(self) -> None:
        DryadsUtil.check_cmd_tree(self.cmd_tree)

    def config(self) -> None:
        # add command 'env'
        if DryadsUtil.cmd_tree_match_opt(self.cmd_tree, "env") is not None:
            raise Exception("[Dryads] The 'env' option conflicts with built-in opts.")
        self.cmd_tree["env"] = DryadsEnv.println
        # add command 'help'
        if (
            DryadsUtil.cmd_tree_match_opt(self.cmd_tree, "-h") is not None
            or DryadsUtil.cmd_tree_match_opt(self.cmd_tree, "--help") is not None
        ):
            raise Exception(
                "[Dryads] The '-h'/'--help' option conflicts with built-in opts."
            )
        self.cmd_tree[("-h", "--help")] = DryadsUtil.help_opt_func_gen(self.cmd_tree)

    def main(self) -> None:
        self.opts = sys.argv[1:]
        if len(self.opts) == 0:
            DryadsUtil.help_opt_func_gen(self.cmd_tree)()
        else:
            self.opt_dfs(self.opts, self.cmd_tree)

    def dfs_run(self, cmds: Union[dict, list, str, Callable]):
        if callable(cmds):
            cmds()
        elif type(cmds) is str:
            DryadsUtil.dryads_run_shell_cmd(cmds)
        elif type(cmds) is list:
            [DryadsUtil.flag_push(ele) for ele in cmds if type(ele) is DryadsFlag]
            [self.dfs_run(ele) for ele in cmds if type(ele) is not DryadsFlag]
            [DryadsUtil.flag_pop(ele) for ele in cmds if type(ele) is DryadsFlag]
        elif type(cmds) is dict:
            [
                DryadsUtil.flag_push(k, v)
                for k, v in cmds.items()
                if type(k) is DryadsFlag
            ]
            [self.dfs_run(v) for k, v in cmds.items() if type(k) is not DryadsFlag]
            [
                DryadsUtil.flag_pop(k, v)
                for k, v in cmds.items()
                if type(k) is DryadsFlag
            ]
        else:
            assert False, cmds

    def opt_dfs(self, opts: list, cmds: Union[dict, Any], path: List[str] = []):
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
                        [ele == DryadsFlag.AcceptArg for ele in cmd_tree_node]
                    ):
                        print(
                            "\033[31m" + "No DryadsArg provided in subtree." + "\033[0m"
                        )
                        exit(-1)

            check_subtree_not_accept_arg_flag(cmds)
            self.dfs_run(cmds)
            return

        if (
            type(cmds) is not dict  # 叶子节点
            and len(opts) == 1  # 参数只剩一个
            and type(cmds) is list  # 叶子内容是列表
            and DryadsFlag.AcceptArg in cmds  # DryadsFlag.AcceptArg在其中
        ):
            DryadsContainer.DryadsArg = opts[0]
            self.dfs_run(cmds)
            return

        def internal_match() -> Union[dict, list, str, None]:
            dummy = DryadsUtil.cmd_tree_match_opt(cmds, opts[0])
            if dummy is not None:
                return dummy

            if opts[0] in ("-h", "--help"):
                return DryadsUtil.help_opt_func_gen(cmds, path)

            return None

        if type(cmds) is not dict or internal_match() is None:
            print(f"opts \"{' '.join(self.opts)}\" error", end=", ")
            print(f"unsupported or spelled incorrectly", end=", ")
            print(f'give it a try of option "--help"', end=".\n")
            return

        if DryadsFlag.PrefixCmd in cmds:
            DryadsUtil.flag_push(DryadsFlag.PrefixCmd, cmds[DryadsFlag.PrefixCmd])

        self.opt_dfs(opts[1:], internal_match(), path + [opts[0]])

        if DryadsFlag.PrefixCmd in cmds:
            DryadsUtil.flag_pop(DryadsFlag.PrefixCmd, cmds[DryadsFlag.PrefixCmd])
