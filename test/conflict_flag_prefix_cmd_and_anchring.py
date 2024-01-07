from dryad import Dryad, DryadFlag

cmd_tree = {
    DryadFlag.PrefixCmd: ["cd ..", "mkdir -p .dryad.tmp", "cd .dryad.tmp"],
    "opt": {
        "for-script": "pwd",
        "cur": [DryadFlag.Anchoring, "pwd"],
    },
}

Dryad(cmd_tree)

"""
> python conflict_flag_prefix_cmd_and_anchring.py opt 
pwd
/home/dev/dryad/.dryad.tmp
pwd
/home/dev/dryad/.dryad.tmp

> python ./test/conflict_flag_prefix_cmd_and_anchring.py opt 
pwd
/home/dev/dryad/.dryad.tmp
pwd
/home/dev/.dryad.tmp

先按照DryadFlag.Anchoring跳转到对应路径, 然后执行DryadFlag.PrefixCmd的命令, 最后在执行对应叶子节点的命令
"""
