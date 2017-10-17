#!/usr/bin/env python

from hashlib import sha512
from sys import version_info
from myargon import Argon2id

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

def intestinize(masterpassworddigest, website_name):
    password = masterpassworddigest + website_name.encode('utf_8')
    salt = sha512(website_name.encode('utf-8')).digest()
    digest = Argon2id(salt_len=len(salt),                      
                      salt=salt,
                      hash_len=22,
                      memory_cost=33554,
                      time_cost=100).hash(password)
    del password, salt
    digest = digest[digest.rfind('$')+1:]
    return digest[:30]


    digest = sha512(password).digest()
    return digest

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
        targetRange = list(range(33,47)) + list(range(58,64)) + list(range(91,96)) + list(range(123,126))
    else:
        raise Exception("This characterType is not recognized!")
    character_value = ord(password[i])
    while character_value not in targetRange:
        character_value = (character_value + offset) % 127
    return password[0 : i] + chr(character_value) + password[i+1 : ]

if __name__ == '__main__':
    if version_info > (3, 0): # Python 3
        website_name = input("Enter the website name: ")
    else: # Python 2
        website_name = raw_input("Enter the website name: ")
    
    masterpassworddigest = read_masterpassworddigest()
    
    password = intestinize(masterpassworddigest, website_name)
    
    # We make sure the password will have 1 digit, 1 letter, 1 uppercase letter and 1 symbol
    offset = int(sha512(password.encode('utf-8')).digest().hex(), 16) # Integer value of digest
    indexes_to_pick = find_indexestopick(password, offset)
    password = ensure('digit', password, offset, indexes_to_pick[0])
    password = ensure('lowercase', password, offset, indexes_to_pick[1])
    password = ensure('uppercase', password, offset, indexes_to_pick[2])
    password = ensure('symbol', password, offset, indexes_to_pick[3])
    
    print("=> Your password is: "+str(password))