from dryads import Dryads, DryadsFlag

cmd_tree = {
    DryadsFlag.PrefixCmd: ["cd ..", "mkdir -p .dryads.tmp", "cd .dryads.tmp"],
    "opt": {
        "for-script": "pwd",
        "cur": [DryadsFlag.Anchoring, "pwd"],
    },
}

Dryads(cmd_tree)

"""
> python conflict_flag_prefix_cmd_and_anchring.py opt 
pwd
/home/dev/dryads/.dryads.tmp
pwd
/home/dev/dryads/.dryads.tmp

> python ./test/conflict_flag_prefix_cmd_and_anchring.py opt 
pwd
/home/dev/dryads/.dryads.tmp
pwd
/home/dev/.dryads.tmp

先按照DryadsFlag.Anchoring跳转到对应路径, 然后执行DryadsFlag.PrefixCmd的命令, 最后在执行对应叶子节点的命令
"""
