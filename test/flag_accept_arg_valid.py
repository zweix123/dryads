from dryads import Dryads, DryadsContainer, DryadsFlag


def flag_func():
    """Print dryads arg"""
    print(DryadsContainer.DryadsArg)


cmd_tree = {
    "opt": [
        DryadsFlag.AcceptArg,
        flag_func,
    ]
}


Dryads(cmd_tree)

"""
> python flag_accept_arg_valid.py                     
该脚本命令可分为两大类
  Shell Commands, help会输出命令本身
  Python Function, help会输出函数的__doc__
opt: DryadsFlag.AcceptArg
     Print dryads arg
env: Print Dryads environment variable.
-h/--help: Print commands and desciptions supported by script.py.

> python flag_accept_arg_valid.py opt
[Dryads] No DryadsArg provided in subtree.

> python flag_accept_arg_valid.py opt "Hello World"
Hello World
"""
