from dryads import Dryads, DryadsFlag


def func():
    pass


cmd_tree = {
    "invalid-opt": {
        "1": "echo 1",
        "2": "echo 2",
        "x": [
            DryadsFlag.AcceptArg,
            func,
        ],
    }
}


Dryads(cmd_tree)

"""
> python flag_accept_arg_invalid_func.py 
该脚本命令可分为两大类
  Shell Commands, help会输出命令本身
  Python Function, help会输出函数的__doc__
invalid-opt 1: echo 1
invalid-opt 2: echo 2
invalid-opt x: DryadsFlag.AcceptArg
               None
env: Print Dryads environment variable.
-h/--help: Print commands and desciptions supported by script.py.

> python flag_accept_arg_invalid_func.py invalid-opt
[Dryads] No DryadsArg provided in subtree.

> python flag_accept_arg_invalid_func.py invalid-opt x
[Dryads] No DryadsArg provided in subtree.  # TODO: 这里不太直觉
"""
