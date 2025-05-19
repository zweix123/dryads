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


Dryads(cmd_tree)  # type: ignore

"""
> python flag_ignore_err.py err-interrupt
error-command
bash: line 2: error-command: command not found
Fail

> python flag_ignore_err.py err-continue 
error-command
bash: line 1: error-command: command not found
error-command
bash: line 1: error-command: command not found
error-command
bash: line 1: error-command: command not found
echo valid command
valid command
"""
