#!/usr/bin/env python3
""" Write configuration to put user install script on PATH
"""

import sys
from argparse import ArgumentParser, RawDescriptionHelpFormatter

from .putils import get_paths, set_path_config, get_user_script_path


def get_parser():
    parser = ArgumentParser(description=__doc__,  # Usage from docstring
                            formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument('-x', '--allow-existing', action='store_true',
                        help='Force config write even if dir already on PATH')
    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()
    us_path = get_user_script_path()
    if (not args.allow_existing) and (us_path in get_paths()):
        sys.stderr.write(f'{us_path} already appears to be on your PATH\n')
        sys.exit(0)
    print(set_path_config(us_path))
    print("""\
Now close all terminals and start a new terminal to load new configuration.""")


if __name__ == '__main__':
    main()
