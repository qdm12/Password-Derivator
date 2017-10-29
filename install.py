import pip
from sys import platform, version_info
from os import environ

python2 = ["pysha3", "mock"]
core = ["argon2_cffi"]
ui = ["kivy", "kivy.deps.sdl2", "kivy.deps.glew", "pyperclip"]
tests = ["nose", "rednose", "coverage", "coveralls"]

def install(packages):
    for package in packages:
        pip.main(['install', package])

if __name__ == '__main__':
    install(core)
    if version_info[0] == 2:
        install(python2)
    if 'TRAVIS' in environ:
        install(tests)
    else:
        install(ui)
        
    if platform == 'windows':
        pass
    if platform.startswith('linux'):
        pass
    if platform == 'darwin': # MacOS
        pass