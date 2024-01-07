from dryad import Dryad, DryadFlag

cmd_tree = {
    "pwd": {
        "for-script": "pwd",
        "cur": [DryadFlag.Anchoring, "pwd"],
    },
}


Dryad(cmd_tree)

"""
> python flag_anchring.py pwd for-script
pwd
/home/dev/dryad/test

> python flag_anchring.py pwd cur
pwd
/home/dev/dryad/test

> python test/flag_anchring.py pwd for-script
pwd
/home/dev/dryad/test

> python test/flag_anchring.py pwd cur
pwd
/home/dev/dryad
"""
