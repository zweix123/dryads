from dryads import Dryads, DryadsFlag

cmd_tree = {
    "pwd": {
        "for-script": "pwd",
        "cur": [DryadsFlag.Anchoring, "pwd"],
    },
}


Dryads(cmd_tree)  # type: ignore

"""
> python flag_anchring.py pwd for-script
pwd
/home/dev/dryads/examples

> python flag_anchring.py pwd cur
pwd
/home/dev/dryads/examples

> python examples/flag_anchring.py pwd for-script
pwd
/home/dev/dryads/examples

> python examples/flag_anchring.py pwd cur
pwd
/home/dev/dryads
"""
