#!/usr/bin/env python

from hashlib import sha512
from sys import version_info
from itertools import chain

def read_masterpassworddigest():
    try:
        with open('MasterPasswordDigest.txt','rb') as f:
            password_hash = f.read()
    except IOError as e:
        print("There was the following error opening the file MasterPasswordDigest.txt: "+str(e))
        print("Did you run firstrun.py before this program ? (Aborting program)")
        exit(1)
    print("=> Master password hash file loaded.")
    return password_hash

def get_passwordskeleton(masterpassworddigest, website_name, hashiter=3000000):
    password = masterpassworddigest + website_name.encode('utf_8')
    for _ in range(hashiter):
        password = sha512(password).digest()
    return sha512(password).hexdigest() # hex digest to have readable letters and numbers [0-9a-f]

def make_complicated(password, offset):
    password = password[0:30] # otherwise it's too long for some websites
    for i in range(len(password)): # for each character
        character_value = ord(password[i])
        character_value = (character_value + offset) % 127 # makes sure it's < 127
        while character_value < 33: # we want it to be between 33 and 126
            character_value = (character_value + offset) % 127
        new_character = chr(character_value) # we convert back to character, using the ASCII table
        password = password[0:i] + new_character + password[i+1:]
    return password

def find_indexestopick(password, offset):
    indexes_to_pick = []
    index = 1
    for _ in range(4): # digit + letter + uppercase + symbol
        index = (index * offset) % len(password)
        while index in indexes_to_pick: # we want a different index
            index = (index * offset + 1) % len(password)
        indexes_to_pick.append(index)
    return indexes_to_pick

def ensure(characterType, password, offset, i):
    if characterType == 'digit':
        targetRange = range(48,57)
    elif characterType == 'lowercase':
        targetRange = range(97,122)
    elif characterType == 'uppercase':
        targetRange = range(65,90)
    elif characterType == 'symbol':
        targetRange = chain(range(33,47), range(58,64), range(91,96), range(123,126))
    else:
        raise Exception("This characterType is not recognized!")
    character_value = ord(password[i])
    while character_value not in targetRange:
        character_value = (character_value + offset) % 127
    return password[0 : i] + chr(character_value) + password[i+1 : ]

if __name__ == '__main__':
    print("=======================================================================")
    print("======================== PASSWORD DERIVATOR ===========================")
    print("=======================================================================")
    print("")
    if version_info > (3, 0): # Python 3
        website_name = input("Enter the website name your password is for: ")
    else: # Python 2
        website_name = raw_input("Enter the website name your password is for: ")
    
    # The master password digest file is loaded
    masterpassworddigest = read_masterpassworddigest()
    
    # The website-specific password is created
    password = get_passwordskeleton(masterpassworddigest, website_name)
    offset = int(password, 16) # Integer value of digest
    password = make_complicated(password, offset)
    
    # We make sure the password will have 1 digit, 1 letter, 1 uppercase letter and 1 symbol
    indexes_to_pick = find_indexestopick(password, offset)
    password = ensure('digit', password, offset, indexes_to_pick[0])
    password = ensure('lowercase', password, offset, indexes_to_pick[1])
    password = ensure('uppercase', password, offset, indexes_to_pick[2])
    password = ensure('symbol', password, offset, indexes_to_pick[3])
    
    print("=> Your password is: "+str(password))