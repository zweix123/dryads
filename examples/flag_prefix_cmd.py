from dryads import Dryads, DryadsFlag

cmd_tree = {
    DryadsFlag.PrefixCmd: ["cd ~"],
    "opt": ["pwd"],
}

Dryads(cmd_tree)  # type: ignore


"""
> pwd                
/home/dev/dryads/test

> python flag_prefix_cmd.py opt
pwd
/home/dev
"""
