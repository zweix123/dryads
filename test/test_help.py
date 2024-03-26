import re
import sys
import unittest
from io import StringIO

from dryads import DryadsFlag, utils


class StdOutCapture:
    def __enter__(self):
        self.stdout_buffer = StringIO()
        self.original_stdout = sys.stdout
        sys.stdout = self.stdout_buffer
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout = self.original_stdout

    def get_output(self):
        return self.stdout_buffer.getvalue()


def remove_text_color_escape(text: str) -> str:
    pattern = re.compile(r"\x1b\[\d{1,2}(;\d{1,2})?m")
    cleaned_text = re.sub(pattern, "", text)
    return cleaned_text


HELP_PREFIX = """该脚本命令可分为两大类
  Shell Commands, help会输出命令本身
  Python Function, help会输出函数的__doc__
"""


def test_case(self: unittest.TestCase, cmds: dict, ans: str):
    with StdOutCapture() as sc:
        utils.help_opt_func_gen(cmds)()

    self.assertEqual(remove_text_color_escape(sc.get_output()), HELP_PREFIX + ans)


def print_cmds_dict_help(cmds: dict):
    with StdOutCapture() as sc:
        utils.help_opt_func_gen(cmds)()

    print(repr(sc.get_output()))
    print(repr(remove_text_color_escape(sc.get_output())))
    utils.help_opt_func_gen(cmds)()


class TestHelp(unittest.TestCase):
    def test_base(self):
        CMDS = {
            "a": "b",
        }
        test_case(
            self,
            CMDS,
            "a: b\n",
        )

    def test_multi_cmd(self):
        CMDS = {
            "single": [
                "cd ~",
                "pwd",
            ],
            "multi": """
cd ~
pwd""",
        }
        test_case(self, CMDS, "single: cd ~\n        pwd\nmulti: cd ~\n       pwd\n")

    def test_Chinese(self):
        CMDS = {
            "123": {
                "123": "123",
                "中文": "中文",
                "English": "English",
            },
            "中文": {
                "123": "123",
                "中文": "中文",
                "English": "English",
            },
            "English": {
                "123": "123",
                "中文": "中文",
                "English": "English",
            },
        }
        test_case(
            self,
            CMDS,
            "123 123: 123\n123 中文: 中文\n123 English: English\n中文 123: 123\n中文 中文: 中文\n中文 English: English\nEnglish 123: 123\nEnglish 中文: 中文\nEnglish English: English\n",
        )


if __name__ == "__main__":
    unittest.main()
