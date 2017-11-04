from os.path import isfile, realpath
from os import sep
try: 
    from hashlib import sha3_256 # Python 3
except ImportError:    
    from sha3 import sha3_256 # Python 2.7

working_path = realpath(__file__) + sep + '..' + sep + '..'
    
def isMasterpassworddigestfilePresent():
    if isfile(working_path + sep + 'MasterPasswordDigest.txt'):
        return True
    return False

def sha3(value, hexa=False):
    if not isinstance(value, bytes):
        value = value.encode('utf-8')
    obj = sha3_256(value)
    if hexa:
        return obj.hexdigest()
    else:
        return obj.digest()