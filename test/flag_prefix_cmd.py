from dryad import Dryad, DryadFlag

cmd_tree = {
    DryadFlag.PrefixCmd: ["cd ~"],
    "opt": ["pwd"],
}

Dryad(cmd_tree)
