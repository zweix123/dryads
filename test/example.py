from dryads import Dryads, DryadsContainer, DryadsFlag, run_shell_cmd


def create_python():
    """Create Python"""
    run_shell_cmd(f"poetry new {DryadsContainer.DryadsArg}")


def create_rust():
    """Create Rust"""
    run_shell_cmd(f"cargo new {DryadsContainer.DryadsArg}")


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


Dryads(cmd_tree)
