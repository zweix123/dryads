from dryad import Dryad, DryadFlag

cmd_tree = {
    "invalid-opt": DryadFlag.AcceptArg,
}


Dryad(cmd_tree)

"""
> python flag_accept_arg_invalid.py      
...
Exception: [Drayd] DryadFlag should not be used alone.
"""
