import unittest

from dryads import DryadsFlag, utils


class TestCmdCheck(unittest.TestCase):
    def test_opt_type(self):
        msg = "[Dryads] The commands dict's keys only support str, tuple[str] and DryadsFlag."
        CMDS = {
            "a": "",
            "b": "",
            1: "",
            2: "",
        }
        with self.assertRaises(Exception) as context:
            utils.check_cmd_tree(CMDS)
        self.assertEqual(str(context.exception), msg)
        CMDS = {
            "a": "",
            "b": "",
            (1, 2): "",
        }
        with self.assertRaises(Exception) as context:
            utils.check_cmd_tree(CMDS)
        self.assertEqual(str(context.exception), msg)

    def test_opts_have_space(self):
        CMDS = {
            "a b": "",
        }
        with self.assertRaises(Exception) as context:
            utils.check_cmd_tree(CMDS)
        self.assertEqual(
            str(context.exception),
            "[Drayds] There are options have space char in commands dict.",
        )

    def test_conflicting_opts(self):
        CMDS = {
            "a": "",
            ("a", "aa"): "",
        }
        with self.assertRaises(Exception) as context:
            utils.check_cmd_tree(CMDS)
        self.assertEqual(
            str(context.exception),
            "[Drayds] There are conflicting opts in commands dict.",
        )

    def test_leaf(self):
        def func():
            pass

        CMDS = {
            "a": "a",
            "b": ["a", "b"],
            "c": func,
            "d": [func, func],
            "e": ["a", func],
            "f": [(DryadsFlag.PrefixCmd, ["a"])],
        }
        utils.check_cmd_tree(CMDS)

        msg = "[Dryads] The commands dict's leaf node must be str, Callable, [DryadsFlag | str | Callable | (DryadsFlag, [str])]"
        CMDS = {"a": ["a", []]}
        with self.assertRaises(Exception) as context:
            utils.check_cmd_tree(CMDS)
        self.assertEqual(str(context.exception), msg)
        CMDS = {"a": ["a", {}]}
        with self.assertRaises(Exception) as context:
            utils.check_cmd_tree(CMDS)
        self.assertEqual(str(context.exception), msg)
        CMDS = {"a": ["a", set()]}
        with self.assertRaises(Exception) as context:
            utils.check_cmd_tree(CMDS)
        self.assertEqual(str(context.exception), msg)
        CMDS = {"a": ["a", ()]}
        with self.assertRaises(Exception) as context:
            utils.check_cmd_tree(CMDS)
        self.assertEqual(str(context.exception), msg)
        CMDS = {"a": ["a", (1, 1)]}
        with self.assertRaises(Exception) as context:
            utils.check_cmd_tree(CMDS)
        self.assertEqual(str(context.exception), msg)
        CMDS = {"a": ["a", (DryadsFlag.PrefixCmd, 1)]}
        with self.assertRaises(Exception) as context:
            utils.check_cmd_tree(CMDS)
        self.assertEqual(str(context.exception), msg)
        CMDS = {"a": ["a", (DryadsFlag.PrefixCmd, [1])]}
        with self.assertRaises(Exception) as context:
            utils.check_cmd_tree(CMDS)
        self.assertEqual(str(context.exception), msg)


if __name__ == "__main__":
    unittest.main()
