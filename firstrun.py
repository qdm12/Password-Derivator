#!/usr/bin/env python

from hashlib import sha256
from getpass import getpass

print("=======================================================================")
print("=================== PASSWORD DERIVATOR FIRST RUN ======================")
print("====== Your password won't be saved, only its SHA256 hash digest ======")
print("================= This is safe, you can Google it ! ===================")
print("== It is impossible to go from the hash digest back to the password ===")
print("====== Be sure to keep your MasterPasswordDigest.txt safe though ======")
print("=======================================================================")
print()
master_password = getpass("Enter your master password: ")
password_hash = sha256(master_password.encode('utf_8')).digest()
del master_password
print("=> Hash generated.")
with open('MasterPasswordDigest.txt','wb') as f:
    f.write(password_hash) # saved in bytes, so it will render oddly
print("=> Saved to file.")
print("=> DONE. You can now use derivator.py")    