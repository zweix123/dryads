import os
import sys
from enum import Enum, auto
from typing import Callable, Dict, List, Tuple, TypeAlias, Union

argv: List[str] = []


class DryadsFlag(Enum):
    # 作为叶子的值，表示该叶子中的命令都是以执行脚本的路径开始, 默认从脚本所在的路径开始
    Anchoring = auto()
    # Deprecated: 作为叶子的值, 表示该选项还接收一个可选参数, 并将参数放在变量DryadsArg中
    AcceptArg = auto()
    # 作为叶子的值, 表示执行的脚本是否打印, 默认打印, 使用该标志表示不打印
    InVisible = auto()
    # 作为叶子的值, 表示命令执行出错后是否停止, 默认停止, 使用该标志表示不停止
    IgnoreErr = auto()
    # 作为某个节点的键, 其值对应的脚本为其所有兄弟节点的子树中所有脚本的前置脚本
    PrefixCmd = auto()


class DryadsFlagStack:
    def __init__(self):
        self.prefix_cmds: List[str] = []
        self.flags: List[DryadsFlag] = []
        # Using List is to simulate Stack for backtracking, and using Set cannot backtrack

    """
    push and pop are not type hint in data args, because type system can't impl specific dict value type
    """

    def push(self, flag: DryadsFlag, data=None) -> None:
        assert type(flag) is DryadsFlag
        if flag == DryadsFlag.PrefixCmd:
            if type(data) is str:
                self.prefix_cmds.append(data)
            elif type(data) is list:
                self.prefix_cmds.extend(data)
            else:
                assert False, data
        elif (
            flag == DryadsFlag.InVisible
            or flag == DryadsFlag.IgnoreErr
            or flag == DryadsFlag.Anchoring
        ):
            self.flags.append(flag)
        elif flag == DryadsFlag.AcceptArg:  # Deprecated
            pass
        else:
            assert False

    def pop(self, flag: DryadsFlag, data=None):
        assert type(flag) is DryadsFlag
        if flag == DryadsFlag.PrefixCmd:
            if type(data) is str:
                self.prefix_cmds.pop()
            elif type(data) is list:
                for _ in range(len(data)):
                    self.prefix_cmds.pop()
            else:
                assert False, data
        elif (
            flag == DryadsFlag.InVisible
            or flag == DryadsFlag.IgnoreErr
            or flag == DryadsFlag.Anchoring
        ):
            self.flags.pop()
        elif flag == DryadsFlag.AcceptArg:  # Deprecated
            pass
        else:
            assert False

    def contains(self, flag: DryadsFlag) -> bool:
        assert flag != DryadsFlag.PrefixCmd, flag
        return flag in self.flags

    def get_prefix_cmds(self) -> List[str]:
        return self.prefix_cmds


flag_stack = DryadsFlagStack()


class DryadsEnv:
    def __init__(self):
        self.script_path: str = str()  # 脚本所在的路径, 未初始化
        self.call_path: str = os.getcwd()  # 调用脚本的路径

    def println(self) -> None:
        """Print Dryads environment variable."""
        print(f"script path is {self.script_path}")
        print(f"call path is {self.call_path}")
        sys.stdout.flush()


env = DryadsEnv()


#                        DryadsCmdTreeRootType
#                          |               |
#                          |               |
#                          |               |
#                          |               v
#                          |             DryadsCmdTreeInternalNodeType
#                          |                           |
#                          v                           |
# DryadsCmdTreeInternalNodeType                        |
#               |                                      |
#               |                                      |
#               |                                      v
#               |                         DryadsCmdTreeInternalNodeType
#               |                                      |
#               |                                      |
#               v                                      |
#  DryadsCmdTreeInternalNodeType                       |
#               |                                      |
#               |                                      |
#               |                                      v
#               |                    __DryadsCmdTreeInternalNodeFatherLeafType
#               |                                      |
#               |                                      |
#               |                                      |
#               |                                      |
#               v                                      v
#   DryadsCmdTreeLeafNodeType                DryadsCmdTreeLeafNodeType

DryadsCmdTreeLeafNodeSingleType: TypeAlias = Union[
    str,  # shell command
    Callable,  # function
    DryadsFlag,  # dryads flag(mypy trick for recursion, flag can't single appear in leaf node)
]
# Command Tree Leaf Node Type(dict value)
DryadsCmdTreeLeafNodeType: TypeAlias = Union[
    DryadsCmdTreeLeafNodeSingleType,
    List[DryadsCmdTreeLeafNodeSingleType],
]
# Command Tree Internal Node Key Type(dict key)
DryadsCmdTreeInternalNodeKeyType: TypeAlias = Union[
    str,  # sub command
    DryadsFlag,  # dryads flag
    Tuple[str, ...],  # opt sub command
]
# Command Tree Internal Node And Father of Leaf Node Type(dict)
DryadsCmdTreeInternalNodeFatherLeafType: TypeAlias = Dict[
    DryadsCmdTreeInternalNodeKeyType,
    DryadsCmdTreeLeafNodeType,
]
# Command Tree Internal Node And No Father of Leaf Node Type(dict)
DryadsCmdTreeInternalNodeNoFatherLeafType: TypeAlias = Dict[
    DryadsCmdTreeInternalNodeKeyType,
    DryadsCmdTreeInternalNodeFatherLeafType,
]
# Command Tree Internal Node Type(dict)
DryadsCmdTreeInternalNodeType: TypeAlias = Union[
    DryadsCmdTreeInternalNodeNoFatherLeafType,
    DryadsCmdTreeInternalNodeFatherLeafType,
]
# Command Tree Root 3Type(dict)
DryadsCmdTreeRootType: TypeAlias = DryadsCmdTreeInternalNodeType
# Command Tree Type(dict)
DryadsCmdTreeNodeType: TypeAlias = Union[
    DryadsCmdTreeInternalNodeType, DryadsCmdTreeLeafNodeType
]
