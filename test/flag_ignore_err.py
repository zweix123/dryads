from dryads import Dryads, DryadsFlag

cmd_tree = {
    "err-interrupt": [
        "error-command",
        "error-command",
        "error-command",
        "echo valid command",
    ],
    "err-continue": [
        DryadsFlag.IgnoreErr,
        "error-command",
        "error-command",
        "error-command",
        "echo valid command",
    ],
}


Dryads(cmd_tree)

"""
> python flag_ignore_err.py err-interrupt
error-command
Fail
...

> python flag_ignore_err.py err-continue 
error-command
...
error-command
...
error-command
...
echo valid command
valid command
"""
