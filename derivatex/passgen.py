#!/usr/bin/env python

from math import ceil
from os import sep
from derivatex.tools import sha3, working_path
from derivatex.myargon import Argon2id
from derivatex.initiate import checksumIsValid
from derivatex.tools import isMasterpassworddigestfilePresent
from derivatex.commandLine import passgenCommandLine

class MasterPasswordDigestException(Exception):
    pass

def read_masterpassworddigest():
    if not isMasterpassworddigestfilePresent():
        raise MasterPasswordDigestException("File not found")
    try:
        with open(working_path + sep + 'MasterPasswordDigest.txt','rb') as f:
            digest_and_checksum = f.read()
    except IOError as e:
        raise MasterPasswordDigestException(str(e))
    else:
        if not checksumIsValid(digest_and_checksum):
            raise MasterPasswordDigestException("Checksum error")
        else:
            digest = digest_and_checksum[:-4]
            return digest

def intestinize(masterpassworddigest, website_name, short):
    """
        Returns a string (not bytes) of readable characters
    """
    Input = masterpassworddigest + website_name
    # can't bruteforce password really so we set time_cost to 1
    salt = sha3(website_name)
    length = 24 # for 24 characters
    if short:
        length = 8 # for 8 characters
    digest = Argon2id(salt=salt,
                      hash_len=ceil(length/1.33),
                      memory_cost=33554,
                      time_cost=1).hash(Input)
    del Input, masterpassworddigest, website_name
    digest = digest[digest.rfind('$')+1:]
    return digest[:length]

def deterministic_random(string, multiplier):
    x = 0
    for c in string:
        x += ord(c)
    return x * multiplier
    

def ensure(characterType, password, i):
    if characterType == 0: # digit
        targetRange = range(48,57)
    elif characterType == 1: # uppercase
        targetRange = range(65,90)
    elif characterType == 2: # lowercase
        targetRange = range(97,122)
    elif characterType == 3: # symbol
        targetRange = list(range(33,47)) + list(range(58,64)) + list(range(91,96)) + list(range(123,126))
    character_value = deterministic_random(password, i)
    while character_value not in targetRange:
        character_value = (character_value + 3) % 127
    return password[0 : i] + chr(character_value) + password[i+1 : ]

def find_characterType(c):
    if c.isdigit():
        return 0
    elif c.isupper():
        return 1
    elif c.islower():
        return 2
    else:
        return 3
    
def ensure_characters(password):
    """
        password is meant to be longer than 3 characters
    """
    passwordHas = [0, 0, 0, 0] # digit, uppercase, lowercase, symbol
    for c in password:
        passwordHas[find_characterType(c)] += 1
    index = 3 # serves as multiplier in deterministic_random
    for characterType in range(len(passwordHas)):
        if passwordHas[characterType] == 0:
            # print("Character type "+characterType+" is missing")
            index = deterministic_random(password, index) % len(password)
            while passwordHas[find_characterType(password[index])] <= 1:
                index = (index + 3) % len(password)
            password = ensure(characterType, password, index) 
    return password

def passgen(website_name, short=False):
    website_name = website_name.encode('utf-8')
    masterpassworddigest = read_masterpassworddigest()
    password = intestinize(masterpassworddigest, website_name, short)
    # We make sure the password will have 1 digit, 1 letter, 1 uppercase letter and 1 symbol
    password = ensure_characters(password)
    return password

if __name__ == '__main__':
    passgenCommandLine()