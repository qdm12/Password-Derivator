#!/usr/bin/env python

from hashlib import sha512
from getpass import getpass
from time import time


print("=======================================================================")
print("=================== PASSWORD DERIVATOR FIRST RUN ======================")
print("====== Your password won't be saved, only its SHA512 hash digest ======")
print("================= This is safe, you can Google it ! ===================")
print("== It is impossible to go from the hash digest back to the password ===")
print("====== Be sure to keep your MasterPasswordDigest.txt safe though ======")
print("=======================================================================")
print("")
master_password = "x"
master_password2 = "y"
while master_password != master_password2:
    master_password = getpass("Enter your master password: ")
    master_password2 = getpass("Enter your master password again: ")
    if master_password != master_password2:
        print("Passwords are not matching ! Try again.")
password_hash = sha512(master_password.encode('utf_8')).digest()

#################################################################
####### Calculates the robustness of your master password #######
#################################################################
# TODO: Check if password contains dictionary words
# Checks if the word is part of the english dictionary
with open('english.txt', 'r') as f:
    data = f.read()
    words = set(data.split('\n'))
if master_password in words:
    possible_combinations = len(words)
else: # calculates in robustness if it is not a dictionary word 
    L = len(master_password)
    possible_characters = 0
    for character in master_password:
        if character.isdigit():
            possible_characters += 10
        elif character.isupper():
            possible_characters += 26
        elif character.islower():
            possible_characters += 26
        else: # Symbol
            possible_characters += 28
    possible_combinations = pow(possible_characters, L)
    del possible_characters, L
del master_password

#################################################################
############### Calculates many SHA512 of password ##############
#################################################################
iterations = 5000000
start = time()
for i in range(iterations): # should take about
    password_hash = sha512(password_hash).digest()
    if (i + 1) % (iterations/10) == 0:
        print("=> "+str(100*((i+1)/float(iterations))) + " % of password digests generated")
digest_generation = time()-start

#################################################################
############### Time Robustness of master password ##############
#################################################################
print("=> Digest generation took "+str(digest_generation) + " seconds.")
time_needed1 = round( (digest_generation * possible_combinations) / 31536000, 3)
time_needed2 = round( time_needed1 * 1.2 , 3)
print("=> If an attacker obtains your MasterPasswordDigest file, it will take " + str(time_needed1) + " years for the attacker to find the master password if he uses your computer to do the computations")
print("=> If an attacker knows you use this program and obtains one of your generated passwords, it will take " + str(time_needed2) + " years for the attacker to find the master password if he uses your computer to do the computations")
del possible_combinations
with open('MasterPasswordDigest.txt','wb') as f:
    f.write(password_hash) # saved in bytes, so it will render oddly
print("=> Saved to file.")
print("=> DONE. You can now use derivator.py")    