from dryad import Dryad, DryadFlag


def func():
    pass


cmd_tree = {
    "invalid-opt": {
        "1": "echo 1",
        "2": "echo 2",
        "x": [
            DryadFlag.AcceptArg,
            func,
        ],
    }
}


Dryad(cmd_tree)

"""
> python flag_accept_arg_invalid2.py invalid-opt
No DryadArg provided in subtree.
"""
