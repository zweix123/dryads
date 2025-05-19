from dryads import Dryads, DryadsFlag

cmd_tree = {
    "vis-cmd": [
        "echo 1",
        "echo 2",
        "echo 3",
    ],
    "invis-cmd": [
        DryadsFlag.InVisible,
        "echo 1",
        "echo 2",
        "echo 3",
    ],
}


Dryads(cmd_tree)  # type: ignore

"""
> python flag_invisiable.py vis-cmd
echo 1
1
echo 2
2
echo 3
3

> python flag_invisiable.py invis-cmd
1
2
3
"""
