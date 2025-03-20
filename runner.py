import os
import sys
import subprocess

import keyboard

from main import SETTINGS

def get_venv():
    venv_dir = os.path.join(os.getcwd(), '.venv')

    if sys.platform == 'win32':
        executable = os.path.join(venv_dir, 'Scripts', 'python.exe')
    else:
        executable = os.path.join(venv_dir, 'bin', 'python')
    return executable

VENV_PYTHON = get_venv()

def run_translator():
    path = os.path.abspath('main.py')
    subprocess.Popen([VENV_PYTHON, path])


keyboard.add_hotkey(SETTINGS['Start hot key'], run_translator)

keyboard.wait(SETTINGS['Exit hot key'])