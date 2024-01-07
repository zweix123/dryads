from dryad import Dryad, DryadContainer, DryadFlag


def flag_func():
    """Print dryad arg"""
    print(DryadContainer.DryadArg)


cmd_tree = {
    "opt": [
        DryadFlag.AcceptArg,
        flag_func,
    ]
}


Dryad(cmd_tree)

"""
> python flag_accept_arg_valid.py opt
No DryadArg provided in subtree.

> python flag_accept_arg_valid.py opt "Hello World"
Hello World
"""
