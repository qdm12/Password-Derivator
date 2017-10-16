#!/usr/bin/env python

from robustness import evaluatePassword

from hashlib import sha512
from getpass import getpass
from math import log
     
if __name__ == '__main__':
    master_password = ""
    master_password2 = "x"
    while master_password != master_password2:
        master_password = getpass("Enter your master password: ")
        master_password2 = getpass("Enter your master password again: ")
        if master_password != master_password2:
            print("Passwords are not matching ! Try again.\n")
    del master_password2
    
    possible_combinations = evaluatePassword(master_password)
    print("=> Your password is one of "+str(possible_combinations)+" possible combinations.")
    print("=> Your password has a security of "+str(round(log(possible_combinations, 2),2))+" bits.")
    print("=> Your password is similar to a suitcase lock of "+str(round(log(possible_combinations, 10),1))+" digits.")
    del possible_combinations
    
    password_hash = sha512(master_password.encode('utf_8')).digest()
    del master_password
    iterations = 100
    for i in range(iterations): # should take about
        password_hash = sha512(password_hash).digest()
        if (i + 1) % (iterations/10) == 0:
            print("=> "+str(100*((i+1)/float(iterations))) + " % of password digests generated")
    
    with open('MasterPasswordDigest.txt','wb') as f:
        f.write(password_hash) # saved in bytes, so it will render oddly
    print("=> Saved to file.")
    print("=> DONE. You can now use derivatex.py")