import unittest

import dryads.checker as checker
from dryads import DryadsFlag


class TestCheck(unittest.TestCase):
    def test_check_sub_cmd(self):
        test_cases = [
            (42, "[dryads.check] The sub command must be a str."),
            ("", "[dryads.check] The sub command must be a non-empty str."),
            (" ", "[dryads.check] The sub command must not contain space."),
        ]
        for test_case in test_cases:
            with self.assertRaises(Exception) as context:
                checker._check_sub_cmd(test_case[0])  # type: ignore
            self.assertEqual(str(context.exception), test_case[1])

    def test_check_multi_choice_sub_cmd(self):
        test_cases = [
            (
                1,
                "[dryads.check] The optional sub command must be a tuple.",
            ),
            (
                ("s"),
                "[dryads.check] The optional sub command must be a tuple.",
            ),
            (
                (),
                "[dryads.check] The optional sub command must be a non-empty tuple.",
            ),
            (
                ("s", 42),
                "[dryads.check] The optional sub command must be a tuple of str.",
            ),
            (
                ("s", "s"),
                "[dryads.check] The optional sub command must be a tuple of unique str.",
            ),
        ]

        for test_case in test_cases:
            with self.assertRaises(Exception) as context:
                checker._check_multi_choice_sub_cmd(test_case[0])  # type: ignore
            self.assertEqual(
                str(context.exception),
                test_case[1],
            )

    def test_check_dryads_flag_internal(self):
        # Too simple, not tested
        checker._check_dryads_flag_internal(DryadsFlag.PrefixCmd)

    def test_check_dryads_flag_leaf(self):
        # Too simple, not tested
        checker._check_dryads_flag_leaf(DryadsFlag.Anchoring)

    def test_check_shell_cmd(self):
        checker._check_shell_cmd("")

    def test_check_func(self):
        def f():
            pass

        checker._check_func(f)

    def test_check_cmd_tree(self):
        test_cases = [
            (
                {1: ""},
                "[dryads.check] The command tree internal node keys only support str, DryadsFlag or tuple[str].",
            ),
            (
                {(1): ""},
                "[dryads.check] The command tree internal node keys only support str, DryadsFlag or tuple[str].",
            ),
            (
                {
                    "1": "",
                    "2": "",
                    ("1", "2"): "",
                },
                "[dryads.check] sub command conflicts.",
            ),
            (
                {"a": ["a", []]},
                "[dryads.check] The command tree leaf node must be str, Callable, DryadsFlag or list of them.",
            ),
            (
                {"a": ["a", {}]},
                "[dryads.check] The command tree leaf node must be str, Callable, DryadsFlag or list of them.",
            ),
            (
                {"a": ["a", set()]},
                "[dryads.check] The command tree leaf node must be str, Callable, DryadsFlag or list of them.",
            ),
            (
                {"a": ["a", ()]},
                "[dryads.check] The command tree leaf node must be str, Callable, DryadsFlag or list of them.",
            ),
            (
                {"a": ["a", (1, 1)]},
                "[dryads.check] The command tree leaf node must be str, Callable, DryadsFlag or list of them.",
            ),
            (
                {"a": ["a", (DryadsFlag.PrefixCmd, 1)]},
                "[dryads.check] The command tree leaf node must be str, Callable, DryadsFlag or list of them.",
            ),
            (
                {"a": ["a", (DryadsFlag.PrefixCmd, [1])]},
                "[dryads.check] The command tree leaf node must be str, Callable, DryadsFlag or list of them.",
            ),
        ]
        for test_case in test_cases:
            with self.assertRaises(Exception) as context:
                checker.check_cmd_tree(test_case[0])  # type: ignore
            self.assertEqual(
                str(context.exception),
                test_case[1],
            )

        def f():
            pass

        cmds = {
            "a": "a",
            "b": ["a", "b"],
            "c": f,
            "d": [f, f],
            "e": ["a", f],
            "f": [DryadsFlag.IgnoreErr, "a"],
            # "f": [(DryadsFlag.IgnoreErr, ["a"])],  #?
        }

        checker.check_cmd_tree(cmds)  # type: ignore


if __name__ == "__main__":
    unittest.main()
