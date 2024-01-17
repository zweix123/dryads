import os
import subprocess
import sys

FILEPATH = os.path.join(os.path.expanduser("~"), "dryadsfile")


def main():
    if not os.path.exists(FILEPATH):
        print(f"file {FILEPATH} not exists.")
        exit(-1)
    subprocess.call([sys.executable, FILEPATH, *sys.argv[1:]])


if __name__ == "__main__":
    main()
