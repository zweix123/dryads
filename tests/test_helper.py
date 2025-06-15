import re
import sys
import unittest
from io import StringIO

from dryads.helper import _help_cmd_func


class StdOutCapture:
    def __enter__(self):
        self.stdout_buffer = StringIO()
        self.original_stdout = sys.stdout
        sys.stdout = self.stdout_buffer
        return self

    def __exit__(self, *args):
        sys.stdout = self.original_stdout

    def get(self):
        return self.stdout_buffer.getvalue()


def remove_text_color(text: str) -> str:
    pattern = re.compile(r"\x1b\[\d{1,2}(;\d{1,2})?m")
    cleaned_text = re.sub(pattern, "", text)
    return cleaned_text


class TestHelp(unittest.TestCase):
    def test_TDT(self):
        test_cases: list[dict] = [
            {
                "name": "empty",
                "args": {},
                "want": "",
            },
            {
                "name": "common",
                "args": {
                    "a": "b",
                },
                "want": "a: b\n",
            },
            {
                "name": "typical",
                "args": {
                    "single": [
                        "cd ~",
                        "pwd",
                    ],
                    "multi": """
cd ~
pwd""",
                    "indentation": """cd ~
pwd""",
                },
                "want": "single: cd ~\n        pwd\nmulti: cd ~\n       pwd\nindentation: cd ~\n             pwd\n",
            },
            {
                "name": "中文",
                "args": {
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
                },
                "want": "123 123: 123\n123 中文: 中文\n123 English: English\n中文 123: 123\n中文 中文: 中文\n中文 English: English\nEnglish 123: 123\nEnglish 中文: 中文\nEnglish English: English\n",
            },
        ]

        for test_case in test_cases:
            with self.subTest(test_case["name"]):
                with StdOutCapture() as soc:
                    _help_cmd_func(test_case["args"], [])
                output = soc.get()
                print(output)
                print(test_case["want"])
                self.assertEqual(test_case["want"], remove_text_color(output))


if __name__ == "__main__":
    unittest.main()
