from dryads import Dryads, DryadsContainer, DryadsFlag


def flag_func():
    """Print dryads arg"""
    print(DryadsContainer.DryadsArg)


cmd_tree = {
    "opt": [
        DryadsFlag.AcceptArg,
        flag_func,
    ]
}


Dryads(cmd_tree)

"""
> python flag_accept_arg_valid.py opt
No DryadsArg provided in subtree.

> python flag_accept_arg_valid.py opt "Hello World"
Hello World
"""
