import sys
import unittest

from dryads import Dryads, DryadsFlag


def f():
    """This F"""
    pass


class TestCheck(unittest.TestCase):
    def setUp(self):
        # 保存原始的sys.argv
        self.original_argv = sys.argv.copy()

    def tearDown(self):
        # 测试后恢复原始的sys.argv
        sys.argv = self.original_argv

    def test_init(self):
        cmds = {
            "a": "a",
            "b": ["a", "b"],
            "c": f,
            "d": [f, f],
            "e": ["a", f],
            "f": [DryadsFlag.IgnoreErr, "a"],
        }
        Dryads(cmds)  # type: ignore


if __name__ == "__main__":
    unittest.main()
