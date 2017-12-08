import pip
from sys import version_info

pipOptions = ['-q']

def install(packages):
    for package in packages:
        pip.main(['install', package] + pipOptions)
        
def core():
    install(["argon2_cffi"])
    if version_info[0] == 2:
        install("pysha3")
        
def passgenCommandLine():
    install(["qrcode", "pyperclip"])
        
def kivy():
    install(["kivy", "kivy.deps.sdl2", "kivy.deps.glew"])
        
def dev():
    install(["nose", "rednose", "coverage", "coveralls"])
    if version_info[0] == 2:
        install(["mock"])
        
if __name__ == '__main__':
    pipOptions = [] # not quiet
    core()
    passgenCommandLine()
    dev()
    kivy()