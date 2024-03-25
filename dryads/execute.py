import os
import subprocess
import sys

from .common import DryadsEnv


def main():
    DRYADSFILE = "dryadsfile"

    dirpath = DryadsEnv.CALLPATH

    while os.sep in dirpath:
        filepath = os.path.join(dirpath, DRYADSFILE)

        if os.path.exists(filepath):
            break
        dirpath = os.sep.join(dirpath.split(os.sep)[:-1])

    if os.sep not in dirpath:
        print(f"Can't find dryadsfile.")
        exit(-1)

    filepath = os.path.join(dirpath, DRYADSFILE)
    subprocess.call([sys.executable, filepath, *sys.argv[1:]])


if __name__ == "__main__":
    main()
