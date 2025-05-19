import dryads
from dryads import Dryads, DryadsFlag, run_shell_cmd


def create_python():
    """Create Python"""
    run_shell_cmd(f"poetry new {dryads.argv[0]}")


def create_rust():
    """Create Rust"""
    run_shell_cmd(f"cargo new {dryads.argv[0]}")


cmd_tree = {
    "echo": {
        "English": "echo Hello World",
        "Chinese": "echo 我可以吞下玻璃而不受到伤害",
        "Math": ["echo 42", "echo 3.14"],
    },
    "work": {
        DryadsFlag.PrefixCmd: ["cd Project"],
        "build": "cd build && make -j`nproc`",
        "run": "./build/bin/work",
    },
    "create": {
        "python": [
            DryadsFlag.Anchoring,
            DryadsFlag.AcceptArg,
            create_python,
        ],
        "rust": [
            DryadsFlag.Anchoring,
            DryadsFlag.AcceptArg,
            create_rust,
        ],
    },
    ("-ds", "--dryads"): "echo Hello Dryads",
}


Dryads(cmd_tree)  # type: ignore

"""
> python typical.py       
该脚本命令可分为两大类
  Shell Commands, help会输出命令本身
  Python Function, help会输出函数的__doc__
echo English: echo Hello World
echo Chinese: echo 我可以吞下玻璃而不受到伤害
echo Math: echo 42
           echo 3.14
work DryadsFlag.PrefixCmd: cd Project
work build: cd build && make -j`nproc`
work run: ./build/bin/work
create python: DryadsFlag.Anchoring
               DryadsFlag.AcceptArg
               Create Python
create rust: DryadsFlag.Anchoring
             DryadsFlag.AcceptArg
             Create Rust
-ds/--dryads: echo Hello Dryads
env: Print Dryads environment variable.
-h/--help: Print commands and desciptions supported by script.py.

> python typical.py echo --help
该脚本命令可分为两大类
  Shell Commands, help会输出命令本身
  Python Function, help会输出函数的__doc__
English: echo Hello World
Chinese: echo 我可以吞下玻璃而不受到伤害
Math: echo 42
      echo 3.14
-h/--help: Print commands and desciptions supported by script.py.
"""
