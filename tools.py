from sys import version_info
from os.path import isfile

def input_compat(message):
    if version_info > (3, 0): # Python 3
        return input(message)
    else: # Python 2
        return raw_input(message)
    
def isMasterpassworddigestfilePresent():
    if isfile("MasterPasswordDigest.txt"):
        return True
    return False