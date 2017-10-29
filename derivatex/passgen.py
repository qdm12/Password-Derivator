#!/usr/bin/env python

from derivatex.tools import sha3
from derivatex.myargon import Argon2id
from derivatex.initiate import checksumIsValid
from derivatex.tools import isMasterpassworddigestfilePresent

try:
    from builtins import input
except ImportError:
    from __builtin__ import raw_input as input

class MasterPasswordDigestException(Exception):
    pass

def read_masterpassworddigest():
    if not isMasterpassworddigestfilePresent():
        raise MasterPasswordDigestException("File not found")
    try:
        with open('MasterPasswordDigest.txt','rb') as f:
            digest_and_checksum = f.read()
    except IOError as e:
        raise MasterPasswordDigestException(str(e))
    else:
        if not checksumIsValid(digest_and_checksum):
            raise MasterPasswordDigestException("Checksum error")
        else:
            digest = digest_and_checksum[:-4]
            return digest

def intestinize(masterpassworddigest, website_name):
    """
        Returns a string (not bytes) of readable characters
    """    
    Input = masterpassworddigest + website_name
    # can't bruteforce password really so we set time_cost to 1
    salt = sha3(website_name)
    digest = Argon2id(salt=salt,
                      hash_len=22, # for 31 characters
                      memory_cost=33554,
                      time_cost=1).hash(Input)
    del Input, masterpassworddigest, website_name
    digest = digest[digest.rfind('$')+1:]
    return digest[:30]

def ensure(characterType, password, i):
    if characterType == 'digit':
        targetRange = range(48,57)
    elif characterType == 'lowercase':
        targetRange = range(97,122)
    elif characterType == 'uppercase':
        targetRange = range(65,90)
    elif characterType == 'symbol':
        targetRange = list(range(33,47)) + list(range(58,64)) + list(range(91,96)) + list(range(123,126))
    character_value = int(sha3(password[i], hexa=True), 16)
    while character_value not in targetRange:
        character_value = (character_value + 3) % 127
    return password[0 : i] + chr(character_value) + password[i+1 : ]

def find_characterType(c):
    if c.isdigit():
        return "digit"
    elif c.isupper():
        return "uppercase"
    elif c.islower():
        return "lowercase"
    else:
        return "symbol"
    
def ensure_characters(password):
    """
        password is meant to be longer than 3 characters
    """
    passwordHas = {"digit":0, "lowercase":0, "uppercase":0, "symbol":0}
    for c in password:
        passwordHas[find_characterType(c)] += 1
    for characterType in passwordHas:
        if passwordHas[characterType] == 0:
            # print("Character type "+characterType+" is missing")
            index = int(sha3(password, hexa=True), 16) % len(password)
            while passwordHas[find_characterType(password[index])] <= 1:
                index = (index + 3) % len(password)
            password = ensure(characterType, password, index) 
    return password

def passgen(website_name):
    website_name = website_name.encode('utf-8')
    masterpassworddigest = read_masterpassworddigest()
    password = intestinize(masterpassworddigest, website_name)
    # We make sure the password will have 1 digit, 1 letter, 1 uppercase letter and 1 symbol
    password = ensure_characters(password)
    return password

if __name__ == '__main__':
    website_name = input("Enter the website name: ")
    password = passgen(website_name)
    print("=> Your password is: "+str(password))