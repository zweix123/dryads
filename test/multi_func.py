from dryads import Dryads, DryadsContainer, DryadsFlag


def example_func():
    print("Call example_func")


def simple_func():
    """This is a simple function."""
    print("Call simple_func")


def complex_func():
    """
         Complex Func
    ========================
       args   ||  none
     ability  ||  print

    不需要参数, 功能仅打印。"""
    print("Call complex_func")


def input_func():
    """Output DryadsArg"""
    assert DryadsContainer.DryadsArg is not None
    print(DryadsContainer.DryadsArg)


cmd_tree = {
    "func": {
        "example": example_func,
        "simple": simple_func,
        "complex": complex_func,
        "input": input_func,
    },
}


Dryads(cmd_tree)
