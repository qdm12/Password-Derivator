#!/usr/bin/env python

from hashlib import sha512
from getpass import getpass
from myargon import Argon2id
from robustness import evaluatePassword

def choose_password():
    password1 = ""
    password2 = ""
    safe = False
    matching = False
    while not matching or not safe:
        password1 = getpass("Enter your master password: ")
        password2 = getpass("Enter your master password again: ")
        matching = (password1 == password2)
        security_bits, security_digits, safe = evaluatePassword(password1)
        if not matching:
            print("Passwords are not matching ! Try again.\n")
        else:
            print("=> Your password has a security of "+str(security_bits)+" bits.")
            print("=> Your password is similar to a suitcase lock of "+str(security_digits)+" digits.")
        if not safe:
            print("=> Your password is not safe. Enter a more complex password.\n")
    del password2
    return password1

def enter_birthdate():
    birthdate1 = ""
    birthdate2 = ""
    matching = False
    while not matching:
        birthdate1 = getpass("Enter your birthdate: ")
        birthdate2 = getpass("Enter your birthdate: ") # check format in UI later
        matching = (birthdate1 == birthdate2)
        if not matching:
            print("Birthdates are not matching ! Try again.\n")
    del birthdate2
    return birthdate1

def intestinize(password, birthdate):
    salt = sha512(birthdate.encode('utf-8')).digest()
    digest = Argon2id(salt_len=len(salt),                      
                      salt=salt).hash(password)
    del password
    digest = digest[digest.rfind('$')+1:]
    return digest
     
def main():
    master_password = choose_password()
    birthdate = enter_birthdate() #"32/43/1999"
    # We want to get rid of the master password ASAP so we hash it (512 to keep entropy)
    digest = sha512(master_password.encode('utf_8')).digest()
    del master_password
    digest = intestinize(digest, birthdate)    
    with open('MasterPasswordDigest.txt','wb') as f:
        f.write(digest.encode('utf-8')) # saved in bytes, so it will render oddly
    print("=> Saved to file.")
    print("=> DONE. You can now use derivatex.py")
    
if __name__ == "__main__":
    main()