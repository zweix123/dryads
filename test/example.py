from dryad import Dryad, DryadContainer, DryadFlag, run_shell_cmd


def create_python():
    """Create Python"""
    run_shell_cmd(f"poetry new {DryadContainer.DryadArg}")


def create_rust():
    """Create Rust"""
    run_shell_cmd(f"cargo new {DryadContainer.DryadArg}")


cmd_tree = {
    "echo": {
        "English": "echo Hello World",
        "Chinese": "echo 我可以吞下玻璃而不收到伤害",
        "Math": ["echo 42", "echo 3.14"],
    },
    "work": {
        DryadFlag.PrefixCmd: ["cd Project"],
        "build": "cd build && make -j`nproc`",
        "run": "./build/bin/work",
    },
    "create": {
        "python": [
            DryadFlag.Anchoring,
            DryadFlag.AcceptArg,
            create_python,
        ],
        "rust": [
            DryadFlag.Anchoring,
            DryadFlag.AcceptArg,
            create_rust,
        ],
    },
    ("-d", "--dryad"): "echo Hello Dryad",
}


Dryad(cmd_tree)
