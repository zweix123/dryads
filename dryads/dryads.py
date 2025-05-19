import inspect
import os
import sys
from typing import Optional

from . import checker, helper, shell
from .common import (
    DryadsCmdTreeInternalNodeType,
    DryadsCmdTreeNodeType,
    DryadsCmdTreeRootType,
    DryadsFlag,
    argv,
    env,
    flag_stack,
)


def match(
    cmd_node: DryadsCmdTreeInternalNodeType, sub_cmd: str
) -> Optional[DryadsCmdTreeNodeType]:
    """单层匹配

    Args:
        cmd_node (DryadsCmdTreeInternalNodeType): _description_
        sub_cmd (str): _description_

    Returns:
        Optional[DryadsCmdTreeNodeType]: _description_
    """
    for k, v in cmd_node.items():
        if (type(k) is str and sub_cmd == k) or (type(k) is tuple and sub_cmd in k):
            return v
    return None


def run_help_cmd_func(cmd_node: DryadsCmdTreeNodeType) -> None:
    # help命令并不是构造在树中, 而是在需要执行时构造并执行
    cmd_node[("-h", "--help")] = helper.gen_help_cmd_func(cmd_node)  # type: ignore
    cmd_node[("-h", "--help")]()  # type: ignore
    # TODO(zweix): 解决这里的类型问题


class Dryads:
    def __init__(self, cmd_tree: DryadsCmdTreeRootType):
        env.script_path = os.path.dirname(inspect.stack()[1].filename)

        if cmd_tree is None:
            raise Exception("cmd_tree is None")
        if not isinstance(cmd_tree, dict):
            raise Exception("cmd_tree is not a dict")

        self.cmd_tree = cmd_tree
        self.sys_argv = sys.argv[1:]

        self.check()
        self.config()
        self.run()

    def check(self) -> None:
        checker.check_cmd_tree(self.cmd_tree)

    def config(self) -> None:
        if "env" not in self.cmd_tree:
            self.cmd_tree["env"] = env.println  # type: ignore

    def run(self) -> None:
        if len(self.sys_argv) == 0:  # 特判
            run_help_cmd_func(self.cmd_tree)
            return
        """
        - 两个阶段:
          1. 第一阶段以参数为递归树的路径, 递归到无法递归为止
          2. 第二阶段以递归到的位置, 执行子树
        
        - 合法的情况
          1. 路径被(真)包含于树拥有的路径 -> 执行子树
          2. 路径的一部分被真包含于树拥有的路径
             1. 剩下的部分有且只有一个且是"-h"/"--help"  -> (子)树helper
          3. 树的一个达到叶子的路径被真包含于路径 -> 执行叶子且路径剩余的部分作为参数
        """

        # 1. 查询阶段:
        cur_node: DryadsCmdTreeNodeType = self.cmd_tree
        for idx, sys_arg in enumerate(self.sys_argv):
            if not isinstance(cur_node, dict):  # 到达叶子
                argv[:] = self.sys_argv[idx:]  # 剩下的部分作为参数
                break
            if DryadsFlag.PrefixCmd in cur_node:
                flag_stack.push(DryadsFlag.PrefixCmd, cur_node[DryadsFlag.PrefixCmd])
            son = match(cur_node, sys_arg)
            if son is not None:  # 匹配到
                cur_node = son
                continue
            # 没有匹配到
            if idx == len(self.sys_argv) - 1 and sys_arg in ("-h", "--help"):
                run_help_cmd_func(cur_node)
                exit(0)
            raise Exception(f"Unknown command: sys.argv[{idx}] = {sys_arg}")

        # 2. 执行阶段
        def dfs(node: DryadsCmdTreeNodeType) -> None:
            if isinstance(node, dict):  # internal node
                for k, v in node.items():
                    if isinstance(k, DryadsFlag):
                        flag_stack.push(k, v)
                for k, v in node.items():
                    if not isinstance(k, DryadsFlag):
                        dfs(v)
                for k, v in node.items():
                    if isinstance(k, DryadsFlag):
                        flag_stack.pop(k, v)
            else:
                if isinstance(node, str):
                    shell.dryads_run_shell_cmd(node)
                elif callable(node):
                    node()
                elif isinstance(node, list):
                    for ele in node:
                        if isinstance(ele, DryadsFlag):
                            flag_stack.push(ele)
                    for ele in node:
                        if not isinstance(ele, DryadsFlag):
                            dfs(ele)
                    for ele in node:
                        if isinstance(ele, DryadsFlag):
                            flag_stack.pop(ele)
                else:
                    assert False, node

        dfs(cur_node)
