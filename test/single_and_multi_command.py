from dryad import Dryad

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

Dryad(cmd_tree)


"""
> python single_and_multi_command.py single
cd ~
pwd
/home/dev/dryad/test

> python single_and_multi_command.py multi

    cd ~
    pwd

/home/dev
"""
