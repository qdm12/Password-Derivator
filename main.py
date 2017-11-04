from sys import argv
from os import chdir, sep
   
if __name__ == "__main__":
    chdir(argv[0] + sep + '..')
    
    if len(argv) == 1:
        from derivatex.ui import launch
        launch()
    else: # command line mode
        from pyperclip import copy
        from derivatex.passgen import passgen
        password = passgen(argv[1])
        copy(password)
        print(password)
        print("Password already copied to your clipboard")
        # TODO add setup option