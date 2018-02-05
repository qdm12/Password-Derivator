from sys import argv
from os import chdir, sep

if __name__ == "__main__":
    chdir(argv[0] + sep + '..')
    if len(argv) == 1: # user interface
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
            from derivatex.commandLine import passgenCommandLine
            passgenCommandLine(argv)