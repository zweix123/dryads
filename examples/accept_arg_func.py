import dryads
from dryads import Dryads, argv


def flag_func():
    """Print dryads arg"""
    print(f"argv: {argv}")
    print(f"dryads.argv: {dryads.argv}")


cmd_tree = {
    "opt": [
        flag_func,
    ]
}


Dryads(cmd_tree)  # type: ignore

"""
> python accept_arg_func.py
该脚本命令可分为两大类
  Shell Commands, help会输出命令本身
  Python Function, help会输出函数的__doc__
opt: Print dryads arg
env: Print Dryads environment variable.
-h/--help: Print commands and desciptions supported by script.py.
"""
"""
> python accept_arg_func.py opt
argv: []
dryads.argv: []
"""
"""
> python accept_arg_func.py opt "Hello World"
argv: ['Hello World']
dryads.argv: ['Hello World']
"""
