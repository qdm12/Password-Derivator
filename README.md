# Password-Derivator

## To do
1. Ask for birth date as a source to the number of iterations
2. Use Argon2id with [argon2_cffi](https://pypi.python.org/pypi/argon2_cffi)
3. Make password robustness check better
    - Add other dictionaries
    - Check for birthdates in password
    - Check for common names of individuals (i.e. Trump)
    - Check for common names of places (i.e. Paris)
4. Do unit tests
5. Explain how secured Derivatex is:
    - Bruteforce attacks
    - Rainbow attacks
    - Botnet/Cloud computing/ASIC based attacks
    - Hacking attacks
        - Website hacked
        - HTTP sniffing
        - HTTPS and NSA backdoors at certificate authorities issuing your keys
    - Loss
6. Finish User interface with [Kivy](https://kivy.org)
7. Make it USB portable
8. Bring support to Android and iOS with [Kivy](https://kivy.org)
9. Write proper documentation and update "What does it do ?"

## Done
- Write/Read of master password digest
- Recovery procedure if the master password digest file is lost
- Password generated matches all website requirements (hopefully)
- Unique password generated for each website

## What does it do, SIMPLIFIED 
1. You input your *password* and *birthdate* **once** to generate the file `MasterPasswordDigest.txt`
   - It is impossible to deduce your *password* or *birthdate* from this file
   - This file should be kept safe
2. Every time you login **or** signup on a website, use the program to generate **another password** by entering the **website name**
   - This password is **always** the same for the same (*password*, *birthdate*, *website*) combination
   - It is impossible to deduce the `MasterPasswordDigest.txt` file **or** the website name from this password
   - This password matches all website's passwords requirements, including at least:
      - 1 lowercase letter
     - 1 uppercase letter
     - 1 digit
     - 1 symbol
     - Equal to 30 characters in length
     - No common words our famous names
	     
## What does it do, LESS SIMPLIFIED
1. The first part of the program stores the *nth* **argon2id** hash digest of your **master password** in a *file* (that should thus be **kept safe** !)
   - *nth* is derived from your birth date
   - This allows you to restore the file from your master password and birth date
   - This should only be ran once when you start using the program, for ease of use
   - We use *argon2id* to avoid botnet / cloud computing / ASICs - based attacks
      - If we would use SHA256, Bitcoin miners may [break it](https://www.reddit.com/r/Bitcoin/comments/1ilx9f/could_bitcoin_be_turned_into_the_worlds_largest/#bottom-comments)
      - Even memory-hard hash algorithms such as Scrypt have now ASICs or can be bruteforced with GPUs
2. The second part of the program prompts you every time for the *website/company name* to generate a password deterministically.
   - This allows you to use this program to generate your password for signup **AND** for login
   - This also uses *argon2id* for better security
3. The generation of the password works as follows:
   - The master password digest is read from your file and concatenated with the website name
   - This is then hashed with *argon2id*
   - An *offset* is set to be equal to the integer value of this digest
   - Only the first 30 characters of this digest are taken, to keep under the password length limit of certain websites
   - For each character of the previously derived hexadecimal digest:
      1. The character is converted to an integer (with *ASCII*)
	  2. The *offset* is added to the character's value
	  3. The result is **MOD 127** so that it will be less than 127 (to avoid non-allowed characters of the ASCII table)
	  4. 2 and 3 are performed again if the result is less than 33 (again, to avoid non-allowed characters)
	  5. The character is replaced by the character corresponding to the value previously calculated. This overall gives a more complex password, if the attacker does not know you used this program.
   - We choose 4 unique indexes in the string of characters to change in the current 30 characters long password
      1. A list of indexes is created and empty.
	  2. The initial index is set to 1
	  3. The following is executed 4 times:
	    1. The index is set to itself times the  *offset* and **MOD 30**
	    2. If the index is in the list of indexes already, 3 is performed again
	    3. The index is added to the list of indexes
   - Finally, for each of these 4 indexes:
      - The character in the password at the first index is ensured to be a digit
	  - The character in the password at the second index is ensured to be a lowercase letter
	  - The character in the password at the third index is ensured to be an uppercase letter
	  - The character in the password at the fourth index is ensured to be a symbol (not any ASCII number though)
4. The password is then shown to the user.

## Why ?
- Always **match password requirements** for websites
- If a website not using password hashing is hacked, the attacker will be limited to this website
- You can re-use this program for all websites, especially if the attacker does not know you use this program (most likely)
- **As long as the attacker does not know you use this program**:
  - Your password is very strong and unbreakable if the attacker attacks a website
  - Plaintext communication (over HTTP) of your password won't reveal any information about your master password or password generation
  - NSA sniffing on HTTPS providers will also not learn any information regarding your master password or password generation
- **If an attacker only knows you use this program** AND has one (or more) of your generated password(s)
  - You are safe depending on your master password. This information is given when running *firstrun.py*.
    For example, the master password **abc12$** is safe for 1253600 years (with a single machine attacking)
- **If an attacker knows you use this program** AND **has your MasterPasswordDigest**:
  - You are safe depending on your master password. This information is given when running *firstrun.py*.
    For example, the master password **abc12$** is safe for 1044700 years (with a single machine attacking)