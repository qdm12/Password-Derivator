#!/usr/bin/env python

from time import time
from os import sep

from derivatex.myargon import Argon2id
from derivatex.robustness import evaluatePassword
from derivatex.tools import sha3, working_path
from derivatex.commandLine import initiateCommandLine

def get_time_per_time_cost(iterations=8):
    start = time()
    Argon2id(time_cost=iterations).hash("xxxxx")
    return (time() - start)/iterations

def check_master_password(master_password1, master_password2):
    valid = True
    safer = True
    if not master_password1 == master_password2:
        return not valid, not safer, "Passwords do not match. Please try again."
    security_bits, security_digits, _safe, _safer = evaluatePassword(master_password1)
    message = "Your password has a security of "+str(security_bits)+" bits, equivalent to " + \
               "a suitcase lock of "+str(security_digits)+" digits. "
    if not _safe:
        return not valid, not safer, message + "This is not safe. Please try again with a more complex password." 
    if not _safer:
        return valid, not safer, message + "Your password has a weak security. " + \
                        "Would you like to enter a more complex password?"
    return valid, safer, message + "Your password is safe, good job."

def get_time_cost(birthdate):
    birthdate = birthdate.split('/')
    offset = int(birthdate[0]) + int(birthdate[1]) + int(birthdate[2])
    time_cost = 1
    while time_cost not in range(80, 120):
        time_cost = (time_cost * offset + 1) % 120
    return time_cost

def intestinize(password, birthdate):
    salt = sha3(birthdate)
    time_cost = get_time_cost(birthdate)
    digest = Argon2id(time_cost=time_cost, salt=salt).hash(password)
    del password
    digest = digest[digest.rfind('$')+1:]
    digest = digest.encode('utf-8') # for concatenating with checksum
    checksum = sha3(digest)[-4:]
    digest += checksum
    return digest

def checksumIsValid(digest):
    try:
        checksum = sha3(digest[:-4])[-4:]
    except TypeError:
        return False # digest is not bytes
    return digest[-4:] == checksum

def setup(master_password, birthdate):
    success = True
    # We want to get rid of the master password ASAP so we hash it (512 to keep entropy)
    digest = sha3(master_password)
    del master_password
    digest = intestinize(digest, birthdate)
    try:
        with open(working_path + sep + 'MasterPasswordDigest.txt','wb') as f:
            f.write(digest)
    except Exception as e:
        return not success, "File writing error (" + str(e) + ")"
    else:
        return success, "The digest file has been saved. You can now use PassGen."
    
if __name__ == "__main__":
    initiateCommandLine()
            
            
            