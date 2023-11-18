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
USER_SCRIPT_PATH = Path(
    sysconfig.get_path("scripts",f"{os.name}_user")
).resolve()


def getout(s):
    return check_output(s, shell=True, text=True).strip()


def get_paths():
    path = os.path.os.environ['PATH']
    return [Path(p).resolve() for p in path.split(os.path.pathsep)]


class ZshConfigger:

    config_name = '.zshrc'

    def __init__(self):
        self.sp_rel = USER_SCRIPT_PATH.relative_to(USER_PATH)
        self.config_path = self.get_config_path()

    def get_config_path(self):
        return USER_PATH / self.config_name

    def write_config(self):
        return self._apply_config(f'''
# Inserted by puser
# Add Python --user script directory to PATH
export PATH="$PATH:${{HOME}}/{self.sp_rel}"
''')

    def _apply_config(self, out_text):
        config_path = self.config_path
        config_text = config_path.read_text() if config_path.is_file() else ''
        if out_text in config_text:
            return f'Configuration already exists in {config_path}'
        config_path.write_text(f'{config_text}\n{out_text}')
        return f'Configuration written to {config_path}'


class CshConfigger(ZshConfigger):

    config_name = '.cshrc'

    def write_config(self):
        return self._apply_config(rf'''
# Inserted by puser
# Add Python --user script directory to PATH
setenv PATH "$PATH\:${{HOME}}/{self.sp_rel}"
''')


class TcshConfigger(CshConfigger):

    config_name = '.tcshrc'


class KshConfigger(ZshConfigger):

    config_name = '.kshrc'


class BashConfigger(ZshConfigger):

    config_name = '.bashrc'


class FishConfigger(CshConfigger):

    def get_config_path(self):
        cfg_home = Path(os.environ.get('XDG_CONFIG_HOME', USER_PATH / '.config'))
        cfg_d = cfg_home / 'fish' / 'conf.d'
        if not cfg_d.is_dir():
            cfg_d.mkdir(parents=True)
        return cfg_d / 'pip_user_path.fish'

    def write_config(self):
        return self._apply_config(f'''
# Inserted by puser
fish_add_path --append --path {{$HOME}}/{self.sp_rel}
''')


SHELL_CONFIGGERS = dict(
    csh=CshConfigger,
    tcsh=TcshConfigger,
    zsh=ZshConfigger,
    bash=BashConfigger,
    ksh=KshConfigger,
    fish=FishConfigger,
)


def make_configger():
    shell = get_mac_shell() if IS_MAC else get_unix_shell()
    configger = SHELL_CONFIGGERS.get(shell)
    if configger is None:
        raise RuntimeError(f'I do not know to configure shell "{shell}"')
    return configger()


def get_mac_shell():
    shell_info = getout('dscl . -read ~/ UserShell')
    return re.match(r'UserShell: (/\w+)+', shell_info).groups()[-1][1:]


def get_unix_shell():
    from getpass import getuser
    shell_info = getout(f'getent passwd {getuser()}')
    return shell_info.split(':')[-1].split('/')[-1]


def set_windows_path_env():
    ps_exe = getout('where powershell')
    var_type = '[System.EnvironmentVariableTarget]::User'
    user_path = getout(
        [ps_exe, '-command',
         f'[Environment]::GetEnvironmentVariable("PATH", {var_type})'])
    getout(
        [ps_exe, '-command',
        '[Environment]::SetEnvironmentVariable("PATH",'
         f'"{user_path};{USER_SCRIPT_PATH}", {var_type})'])
    return 'Configured Windows USER PATH environment variable'
