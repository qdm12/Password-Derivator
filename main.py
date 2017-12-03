from sys import argv
from os import chdir, sep
from qrcode import QRCode

   
if __name__ == "__main__":
    chdir(argv[0] + sep + '..')
    if len(argv) == 1:
        from derivatex.main import launch
        launch()
    else: # command line mode
        from pyperclip import copy
        from derivatex.passgen import passgen
        short = False
        if len(argv) > 2: # optional arguments
            if argv[2] == "short":
                short = True                
        password = passgen(argv[1], short)
        copy(password)
        print(password)
        print("Password already copied to your clipboard")
        print("")
        qr = QRCode(border=1)
        qr.add_data(password)
        qr.print_ascii()
        # TODO add setup option