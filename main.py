from sys import argv
from os import chdir, sep   
import install
from os import environ

if __name__ == "__main__":
    chdir(argv[0] + sep + '..')
    install.core()
    if 'TRAVIS' in environ:
        install.dev()
    elif len(argv) == 1: # user interface
        install.kivy()
        from derivatex.main import launch
        launch()
    else: # command line
        if argv[1] == "#setup":
            from derivatex.commandLine import initiateCommandLine
            try:
                initiateCommandLine()
            except KeyboardInterrupt:
                print("")
        else:
            install.passgenCommandLine()
            from derivatex.commandLine import passgenCommandLine
            passgenCommandLine(argv)