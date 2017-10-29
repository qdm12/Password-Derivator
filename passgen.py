#!/usr/bin/env python

try: 
    from hashlib import sha3_256 # Python 3
except ImportError:    
    from sha3 import sha3_256 # Python 2.7
from myargon import Argon2id
from setup import checksumIsValid
from tools import input_compat, isMasterpassworddigestfilePresent

class MasterPasswordDigestException(Exception):
    pass

def read_masterpassworddigest():
    if not isMasterpassworddigestfilePresent():
        raise MasterPasswordDigestException("File not found")
    try:
        with open('MasterPasswordDigest.txt','rb') as f:
            password_hash = f.read()
    except IOError as e:
        raise MasterPasswordDigestException(str(e))
    else:
        if not checksumIsValid(password_hash):
            raise MasterPasswordDigestException("Checksum error")
        else:
            return password_hash

def intestinize(masterpassworddigest, website_name):
    Input = masterpassworddigest + website_name
    # can't bruteforce password really so we set time_cost to 1
    salt = sha3_256(website_name).digest()
    digest = Argon2id(salt=salt,
                      hash_len=22, # for 31 characters
                      memory_cost=33554,
                      time_cost=1).hash(Input)
    del Input, masterpassworddigest, website_name
    digest = digest[digest.rfind('$')+1:]
    return digest[:30]

def ensure(characterType, password, offset, i):
    if characterType == 'digit':
        targetRange = range(48,57)
    elif characterType == 'lowercase':
        targetRange = range(97,122)
    elif characterType == 'uppercase':
        targetRange = range(65,90)
    elif characterType == 'symbol':
        targetRange = list(range(33,47)) + list(range(58,64)) + list(range(91,96)) + list(range(123,126))
    character_value = ord(password[i])
    while character_value not in targetRange:
        character_value = (character_value + offset) % 127
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
    passwordHas = {"digit":0, "lowercase":0, "uppercase":0, "symbol":0}
    for c in password:
        passwordHas[find_characterType(c)] += 1
    offset = int(sha3_256(password.encode('utf-8')).hexdigest(), 16)
    for characterType in passwordHas:
        if passwordHas[characterType] == 0:
            print("Character type "+characterType+" is missing")
            index = offset % len(password)
            while passwordHas[find_characterType(password[index])] <= 1:
                index = (index*offset +1) % len(password)
            password = ensure(characterType, password, offset, index) 
    return password

def passgen(website_name):
    website_name = website_name.encode('utf-8')
    masterpassworddigest = read_masterpassworddigest()
    password = intestinize(masterpassworddigest, website_name)
    # We make sure the password will have 1 digit, 1 letter, 1 uppercase letter and 1 symbol
    password = ensure_characters(password)
    return password

if __name__ == '__main__':
    website_name = input_compat("Enter the website name: ")
    password = passgen(website_name)
    print("=> Your password is: "+str(password))