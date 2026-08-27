#!/usr/bin/env python3

import sys


def main():

    if "--cli" in sys.argv:
        from interface.cli import main as run
        run()

    else:
        from interface.gui import main as run
        run()


if __name__ == "__main__":
    main()
