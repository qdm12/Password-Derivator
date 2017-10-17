#!/usr/bin/env python

from robustness import evaluatePassword

from hashlib import sha512
from argon2 import PasswordHasher
from getpass import getpass


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

def intestinize(password):
    # see https://argon2-cffi.readthedocs.io/en/stable/parameters.html
    password_hash = PasswordHasher().hash(password)
    del password
    return password_hash
     
if __name__ == '__main__':
    master_password = choose_password()
    # We want to get rid of the master password ASAP so we hash it (512 to keep entropy)
    password_hash = sha512(master_password.encode('utf_8')).digest()
    del master_password
    
    
    """
    for i in range(iterations): # should take about
        password_hash = sha512(password_hash).digest()
        if (i + 1) % (iterations/10) == 0:
            print("=> "+str(100*((i+1)/float(iterations))) + " % of password digests generated")
    """
    password_hash = intestinize(password_hash)
    print(password_hash)
    
    with open('MasterPasswordDigest.txt','wb') as f:
        f.write(password_hash.encode('utf-8')) # saved in bytes, so it will render oddly
    print("=> Saved to file.")
    print("=> DONE. You can now use derivatex.py")