from dryad import Dryad, DryadContainer, DryadFlag


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
    """Output DryadArg"""
    assert DryadContainer.DryadArg is not None
    print(DryadContainer.DryadArg)


cmd_tree = {
    "func": {
        "example": example_func,
        "simple": simple_func,
        "complex": complex_func,
        "input": input_func,
    },
}


Dryad(cmd_tree)
