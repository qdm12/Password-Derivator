#!/usr/bin/env python

from hashlib import sha512
from getpass import getpass
from myargon import Argon2id
from robustness import evaluatePassword
from tools import input_compat, isMasterpassworddigestfilePresent

class Birthdate(object):
    def __init__(self, raw_birthdate):
        fields = raw_birthdate.split('/') # to change or check format
        self.day = int(fields[0])
        self.month = int(fields[1])
        self.year = int(fields[2])
        
    def sum(self):
        return self.day + self.month + self.year
    
    def __repr__(self):
        day = str(self.day) if len(str(self.day)) == 2 else '0' + str(self.day)
        month = str(self.month) if len(str(self.month)) == 2 else '0' + str(self.month)
        year = str(self.year)
        return day + '/' + month + '/' + year

def choose_password():
    password1 = getpass("Enter your master password: ")
    password2 = getpass("Enter your master password again: ")
    return password1, password2

def choose_birthdate():
    return input_compat("Enter your birthdate: ")

def check_master_password(master_password1, master_password2):
    valid = True
    safer = True
    if not master_password1 == master_password2:
        return not valid, not safer, "Passwords do not match. Please try again."
    security_bits, security_digits, safe, _safer = evaluatePassword(master_password1)
    message = "Your password has a security of "+str(security_bits)+" bits, equivalent to " + \
               "a suitcase lock of "+str(security_digits)+" digits. "
    if not safe:
        return not valid, not safer, message + "This is not safe. Please try again with a more complex password." 
    if not _safer:
        return valid, not safer, message + "Your password has a weak security. " + \
                        "Would you like to enter a more complex password?"
    return valid, safer, message + "Your password is safe, good job."

def check_birthdate(birthdate):
    valid = True
    return valid, "Birthdate is valid"

def intestinize(password, birthdate):
    salt = sha512(str(birthdate).encode('utf-8')).digest()
    time_cost = 0
    while time_cost not in range(30, 50):
        time_cost += birthdate.sum() % 50  
    digest = Argon2id(time_cost=time_cost, salt=salt).hash(password)
    del password
    digest = digest[digest.rfind('$')+1:]
    digest = digest + sha512(digest).digest()[0:4] # checksum
    return digest

def checksumIsValid(digest):
    return digest[-4:] == sha512(digest[:-4]).digest()

def setup(master_password, birthdate):
    success = True
    birthdate = Birthdate(birthdate)
    # We want to get rid of the master password ASAP so we hash it (512 to keep entropy)
    digest = sha512(master_password.encode('utf_8')).digest()
    del master_password
    digest = intestinize(digest, birthdate)    
    with open('MasterPasswordDigest.txt','wb') as f:
        f.write(digest.encode('utf-8')) # saved in bytes, so it will render oddly
    with open('MasterPasswordDigest.txt','rb') as f:
        digest = f.read()
    if not checksumIsValid(digest):
        return not success, "The digest file checksum is invalid."
    return success, "The digest file has been saved. You can now use PassGen."

def main():
    success = False
    if isMasterpassworddigestfilePresent():
        if input_compat("Digest file already exists. Do you want to overwrite it? yes/no? [no]: ") != "yes":
            return success
    valid = retry = False
    while not valid or retry:
        master_password1, master_password2 = choose_password()
        valid, safer, message = check_master_password(master_password1, master_password2)
        print(message)
        if valid and not safer:
            retry = input_compat("yes/no? [no]") == 'yes'
    valid = False
    while not valid:
        birthdate = choose_birthdate()
        valid, message = check_birthdate(birthdate)
        print(message)
    retry = False
    while not success or retry:
        success, message = setup(master_password1, birthdate)
        print(message)
        if not success:
            retry = input_compat("Do you want to run the procedure again? [no]") == "yes"
    return success # Re-run entire setup if fail? (failed and we don't want to re-run)

if __name__ == "__main__":
    main()
            
            
            