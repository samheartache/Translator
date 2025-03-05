import os
import subprocess

import keyboard

VENV_PYTHON = os.path.join(os.getcwd(), ".venv", "Scripts", "python.exe")

def run_translator():
    path = os.path.abspath('main.py')
    subprocess.Popen([VENV_PYTHON, path])


keyboard.add_hotkey('ctrl+alt+a', run_translator)

keyboard.wait()