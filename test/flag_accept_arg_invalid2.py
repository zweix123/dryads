from dryads import Dryads, DryadsFlag


def func():
    pass


cmd_tree = {
    "invalid-opt": {
        "1": "echo 1",
        "2": "echo 2",
        "x": [
            DryadsFlag.AcceptArg,
            func,
        ],
    }
}


Dryads(cmd_tree)

"""
> python flag_accept_arg_invalid2.py invalid-opt
No DryadsArg provided in subtree.
"""
