from dryads import Dryads

cmd = {
    "a": {},
    "b": {},
    "c": "pwd",
    "d": {
        "e": "pwd",
    },
}

Dryads(cmd)  # type: ignore

"""
> python empty_internal_node.py
该脚本命令可分为两大类
  Shell Commands, help会输出命令本身
  Python Function, help会输出函数的__doc__
a: {}
b: {}
c: pwd
d e: pwd
env: Print Dryads environment variable.
-h/--help: Print commands and desciptions supported by script.py.
"""
"""
> python empty_internal_node.py a
 
"""
