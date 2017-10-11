# Password-Derivator

## What does it do ?
- For *dummies*: 
   1. It takes your *password* **AND** the *name of the website/company* to generate **another password**
   2. This generated password will **always** be the same for the same (password, website) set
   3. There is then no way to go from this generated password back to your master password OR website/company.
   4. No matter what, this generated password will match all website's passwords requirements, including:
      - 1 lowercase letter
	  - 1 uppercase letter
	  - 1 digit
	  - 1 symbol
	  - Equal to 30 characters in length
- For *advanced users*:
   1. It stores the **5,000,000th SHA512 hash digest of your master password** in a *file* (that should thus be **kept safe** !)
      - This allows you to restore the file from your password
	  - We use SHA512 to avoid bitcoin miners to bruteforce your password, see [this](https://www.reddit.com/r/Bitcoin/comments/1ilx9f/could_bitcoin_be_turned_into_the_worlds_largest/#bottom-comments)
   2. It prompts everytime for the *website/company name* to generate a password, which is deterministic.
      - This allows you to use this program to generate your password for signup **AND** for login
   3. The generation of the password works as follows:
      - The SHA512 digest of your master password is concatenated with the website name
	  - This is then hashed with SHA512 3,000,000 times to take about 2 to 3 seconds.
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


## How to use it ?
1. Make sure you have [Python installed](https://www.python.org/downloads/)
2. Download or `git clone` this repository
3. Run *firstrun.py* to generate your password hash digest file
4. Then run *derivator.py*, by just entering the name of the website.
5. Re-use *derivator.py* to signup on new websites, login to websites you already registered with etc.

## What's next ?
- Check for password robustness better
	- Check for words in passwords
	- Add other dictionaries
	- Check for birthdates
	- Check for common names of individuals
- UI
- Android, iOS apps