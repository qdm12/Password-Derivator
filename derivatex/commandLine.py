def passgenCommandLine(argv=[]):
    from derivatex.passgen import passgen
    if len(argv) == 0 or argv[1] is None:
        website_name = input("Enter the website name: ")
    else:
        website_name = argv[1]
    from pyperclip import copy 
    from qrcode import QRCode
    short = False
    if len(argv) > 2: # optional arguments
        if argv[2] == "short":
            short = True               
    password = passgen(website_name, short)
    copy(password)
    print(password)
    print("")
    print("Password has been copied to your clipboard")
    print("")
    qr = QRCode(border=1)
    qr.add_data(password)
    qr.print_ascii()
    
def initiateCommandLine():
    from derivatex.tools import isMasterpassworddigestfilePresent
    from derivatex.initiate import check_master_password, setup
    from getpass import getpass
    try:
        from builtins import input
    except ImportError:
        from __builtin__ import raw_input as input
    success = False
    if isMasterpassworddigestfilePresent():
        if input("Digest file already exists. Do you want to overwrite it? yes/no? [no]: ") != "yes":
            return
    valid = retry = False
    while not valid or retry:
        master_password1 = getpass("Enter your master password: ")
        master_password2 = getpass("Enter your master password again: ")
        valid, safer, message = check_master_password(master_password1, master_password2)
        print(message)
        if valid and not safer:
            retry = input("yes/no? [no]") == 'yes'
    birthdate = input("Enter your birthdate (dd/mm/yyyy): ")
    retry = False
    while not success or retry:
        print("Computing master digest...")
        success, message = setup(master_password1, birthdate)
        print(message)
        if not success:
            retry = input("Do you want to run the procedure again? [no]") == "yes"