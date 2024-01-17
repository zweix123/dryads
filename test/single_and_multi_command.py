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

Dryads(cmd_tree)


"""
> python single_and_multi_command.py single
cd ~
pwd
/home/dev/dryads/test

> python single_and_multi_command.py multi

    cd ~
    pwd

/home/dev
"""
