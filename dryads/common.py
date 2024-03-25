import os
import sys
from enum import Enum, auto
from typing import Callable, Dict, List, Tuple, Union


class DryadsFlag(Enum):
    Anchoring = auto()  # 作为叶子的值，表示该叶子中的命令都是以执行脚本的路径开始, 默认从脚本所在的路径开始
    AcceptArg = auto()  # 作为叶子的值, 表示该选项还接收一个可选参数, 并将参数放在变量DryadsArg中
    InVisible = auto()  # 作为叶子的值, 表示执行的脚本是否打印, 默认打印, 使用该标志表示不打印
    IgnoreErr = auto()  # 作为叶子的值, 表示命令执行出错后是否停止, 默认停止, 使用该标志表示不停止
    PrefixCmd = auto()  # 作为某个节点的键, 其值对应的脚本为子树中所有脚本的前置脚本


DryadsCmdTreeLeafType = Union[
    str, Callable, List[Union[str, Callable, DryadsFlag, Tuple[DryadsFlag, List[str]]]]
]
DryadsCmdTreeInternalKeyType = Union[str, DryadsFlag, Tuple[str]]
DryadsCmdTreeInternalType = Dict[DryadsCmdTreeInternalKeyType, DryadsCmdTreeLeafType]


class DryadsEnv:
    SCRIPTPATH: str = ""  # in Dryads.init(), by reflection
    CALLPATH: str = os.getcwd()
    OSTYPE: str = sys.platform

    @staticmethod
    def println():
        """Print Dryads environment variable."""
        print("SCRIPTPATH", "=", DryadsEnv.SCRIPTPATH)
        print("CALLPATH  ", "=", DryadsEnv.CALLPATH)
        print("OSTYPE    ", "=", DryadsEnv.OSTYPE)
