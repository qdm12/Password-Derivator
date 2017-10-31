from sys import argv
from os import chdir

chdir(argv[0] + '\..')

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