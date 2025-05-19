from dryads import Dryads

cmd_tree = {
    "single": [
        "cd ~",
        "pwd",
    ],
    "multi": """
    cd ~
    pwd
    """,
}

Dryads(cmd_tree)  # type: ignore


"""
> python example_multi_line_cmd.py 
该脚本命令可分为两大类
  Shell Commands, help会输出命令本身
  Python Function, help会输出函数的__doc__
single: cd ~
        pwd
multi: cd ~
       pwd
env: Print Dryads environment variable.
-h/--help: Print commands and desciptions supported by script.py.

> python example_multi_line_cmd.py single
cd ~
pwd
/home/dev/dryads/test

> python example_multi_line_cmd.py multi 

    cd ~
    pwd
    
/home/dev
"""
