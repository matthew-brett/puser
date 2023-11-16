""" Utilities for command Puser line tools
"""

import os
import sys
import re
import sysconfig
from subprocess import check_output
from pathlib import Path

USER_PATH = Path('~').expanduser()
IS_MAC = sys.platform == 'darwin'


def get_user_script_path():
    script_fname = sysconfig.get_path("scripts",f"{os.name}_user")
    return Path(script_fname).resolve()


def getout(s):
    return check_output(s, shell=True, text=True).strip()


def get_paths():
    path = os.path.os.environ['PATH']
    return [Path(p).resolve() for p in path.split(os.path.pathsep)]


def get_mac_shell():
    shell_info = getout('dscl . -read ~/ UserShell')
    return re.match(r'UserShell: (/\w+)+', shell_info).groups()[-1][1:]


def get_unix_shell():
    from getpass import getuser
    shell_info = getout(f'getent passwd {getuser()}')
    return shell_info.split(':')[-1].split('/')[-1]


def get_posix_configfile():
    shell = get_mac_shell() if IS_MAC else get_unix_shell()
    if shell == 'bash':
        return USER_PATH / ('.bash_profile' if IS_MAC else '.bashrc')
    elif shell == 'zsh':
        return USER_PATH / '.zshrc'
    else:
        raise RuntimeError(f'Unexpected shell {shell}')


def set_windows_path_env(site_path):
    ps_exe = getout('where powershell')
    var_type = '[System.EnvironmentVariableTarget]::User'
    user_path = getout(
        [ps_exe, '-command',
         f'[Environment]::GetEnvironmentVariable("PATH", {var_type})'])
    getout(
        [ps_exe, '-command',
        '[Environment]::SetEnvironmentVariable("PATH",'
         f'"{user_path};{site_path}", {var_type})'])


def set_path_config(site_path):
    if sys.platform == 'win32':
        set_windows_path_env(site_path)
        return
    sp_rel = site_path.relative_to(USER_PATH)
    out_text = f'''
# Inserted by configure_shell
# Add Python --user script directory to PATH
export PATH="$PATH:${{HOME}}/{sp_rel}"
'''
    config_path = get_posix_configfile()
    config_text = config_path.read_text()
    if out_text in config_text:
        return f'Configuration already exists in {config_path}'
    config_path.write_text(f'{config_text}\n{out_text}')
    return f'Configuration written to {config_path}'
