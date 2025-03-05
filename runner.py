import os
import subprocess

import keyboard

from main import SETTINGS

VENV_PYTHON = os.path.join(os.getcwd(), ".venv", "Scripts", "python.exe")

def run_translator():
    path = os.path.abspath('main.py')
    subprocess.Popen([VENV_PYTHON, path])


keyboard.add_hotkey(SETTINGS["Hot key"], run_translator)

keyboard.wait('alt+escape')