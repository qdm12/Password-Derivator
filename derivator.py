#!/usr/bin/env python

from hashlib import sha512
from sys import version_info

print("=======================================================================")
print("======================== PASSWORD DERIVATOR ===========================")
print("=======================================================================")
print("")

if version_info > (3, 0): # Python 3
    website_name = input("Enter the website name your password is for: ")
else: # Python 2
    website_name = raw_input("Enter the website name your password is for: ")

try:
    with open('MasterPasswordDigest.txt','rb') as f:
        password_hash = f.read()
except IOError as e:
    print("There was the following error opening the file MasterPasswordDigest.txt: "+str(e))
    print("Did you run firstrun.py before this program ? (Aborting program)")
    exit(1)
print("=> Master password hash file loaded.")

password = password_hash + website_name.encode('utf_8')

for _ in range(3000000):
    password = sha512(password).digest()
    
password = sha512(password).hexdigest() # hex digest to have readable letters and numbers [0-9a-f]

offset = int(password, 16) # Integer value of digest

password = password[0:30] # otherwise it's too long for some websites

for i in range(len(password)):
    character_value = ord(password[i])
    character_value = (character_value + offset) % 127 # makes sure it's < 127
    while character_value < 33: # we want it to be between 33 and 126
        character_value = (character_value + offset) % 127
    new_character = chr(character_value) # we convert back to character, using the ASCII table
    password = password[0:i] + new_character + password[i+1:]

# We make sure the password will have 1 digit, 1 letter, 1 uppercase letter and 1 symbol
indexes_to_pick = []
index = 1
for _ in range(4): # digit + letter + uppercase + symbol
    index = (index * offset) % len(password)
    while index in indexes_to_pick: # we want a different index
        index = (index * offset + 1) % len(password)
    indexes_to_pick.append(index)
    
# Digit
i = indexes_to_pick[0]
character_value = ord(password[i])
while character_value not in range(48,57):
    character_value = (character_value + offset) % 127
password = password[0 : i] + chr(character_value) + password[i+1 : ]
        
# Lowercase letter
i = indexes_to_pick[1]
character_value = ord(password[i])
while character_value not in range(97,122):
    character_value = (character_value + offset) % 127
password = password[0 : i] + chr(character_value) + password[i+1 : ]
    
# Uppercase letter
i = indexes_to_pick[2]
character_value = ord(password[i])
while character_value not in range(65,90):
    character_value = (character_value + offset) % 127
password = password[0 : i] + chr(character_value) + password[i+1 : ]
   
# Symbol
i = indexes_to_pick[3]
character_value = ord(password[i])
while character_value not in range(33,47) and character_value not in range(58,64) and character_value not in range(91,96) and character_value not in range(123,126):
    character_value = (character_value + offset) % 127
password = password[0 : i] + chr(character_value) + password[i+1 : ]

print("=> Your password is: "+str(password))