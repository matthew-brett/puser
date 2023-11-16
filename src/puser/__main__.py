#!/usr/bin/env python3
""" Write configuration to put user install script on PATH
"""

import sys
from argparse import ArgumentParser, RawDescriptionHelpFormatter

from .putils import (get_paths, USER_SCRIPT_PATH, set_windows_path_env,
                     make_configger)


def get_parser():
    parser = ArgumentParser(description=__doc__,  # Usage from docstring
                            formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument('-x', '--allow-existing', action='store_true',
                        help='Force config write even if dir already on PATH')
    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()
    if (not args.allow_existing) and (USER_SCRIPT_PATH in get_paths()):
        sys.stderr.write(
            f'{USER_SCRIPT_PATH} already appears to be on your PATH\n')
        sys.exit(0)
    print(set_windows_path_env() if sys.platform == 'win32'
          else make_configger().write_config())
    print("""\
Now close all terminals and start a new terminal to load new configuration.""")


if __name__ == '__main__':
    main()
