#!/usr/bin/env python

try: 
    from hashlib import sha3_256 # Python 3
except ImportError:    
    from sha3 import sha3_256 # Python 2.7
from getpass import getpass
from myargon import Argon2id
from robustness import evaluatePassword
from tools import input_compat, isMasterpassworddigestfilePresent
from time import time

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
    time_cost = 0
    while time_cost not in range(80, 120):
        time_cost = (time_cost + offset) % 120
    return time_cost

def intestinize(password, birthdate):
    salt = sha3_256(birthdate.encode('utf-8')).digest()
    time_cost = get_time_cost(birthdate)
    digest = Argon2id(time_cost=time_cost, salt=salt).hash(password)
    del password
    digest = digest[digest.rfind('$')+1:]
    digest = digest.encode('utf-8')
    checksum = sha3_256(digest).digest()[-4:]
    digest += checksum
    return digest

def checksumIsValid(digest):
    if type(digest) is not bytes:
        return False
    return digest[-4:] == sha3_256(digest[:-4]).digest()[-4:]

def setup(master_password, birthdate):
    success = True
    # We want to get rid of the master password ASAP so we hash it (512 to keep entropy)
    digest = sha3_256(master_password.encode('utf_8')).digest()
    del master_password
    digest = intestinize(digest, birthdate)
    try:
        with open('MasterPasswordDigest.txt','wb') as f:
            f.write(digest)
    except Exception as e:
        return not success, "File writing error (" + str(e) + ")"
    else:
        return success, "The digest file has been saved. You can now use PassGen."

def main():
    success = False
    if isMasterpassworddigestfilePresent():
        if input_compat("Digest file already exists. Do you want to overwrite it? yes/no? [no]: ") != "yes":
            return success
    valid = retry = False
    while not valid or retry:
        master_password1 = getpass("Enter your master password: ")
        master_password2 = getpass("Enter your master password again: ")
        valid, safer, message = check_master_password(master_password1, master_password2)
        print(message)
        if valid and not safer:
            retry = input_compat("yes/no? [no]") == 'yes'
    birthdate = input_compat("Enter your birthdate (dd/mm/yyyy): ")
    retry = False
    while not success or retry:
        success, message = setup(master_password1, birthdate)
        print(message)
        if not success:
            retry = input_compat("Do you want to run the procedure again? [no]") == "yes"
    return success # Re-run entire setup if fail? (failed and we don't want to re-run)

if __name__ == "__main__":
    main()
            
            
            