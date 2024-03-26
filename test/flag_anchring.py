from dryads import Dryads, DryadsFlag

cmd_tree = {
    "pwd": {
        "for-script": "pwd",
        "cur": [DryadsFlag.Anchoring, "pwd"],
    },
}


Dryads(cmd_tree)

"""
> python flag_anchring.py pwd for-script           
pwd
/home/dev/dryads/test

> python flag_anchring.py pwd cur       
pwd
/home/dev/dryads/test

> python test/flag_anchring.py pwd for-script
pwd
/home/dev/dryads/test

> python test/flag_anchring.py pwd cur       
pwd
/home/dev/dryads
"""
