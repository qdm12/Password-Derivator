from math import log

class WordFound(object):
    def __init__(self, word, start):
        self.start = start
        self.end = start + len(word)
        self.word = word.lower()
        self.hasLowercase = False
        self.hasUppercase = False
        
    def contains(self, other):
        if other.start >= self.start and other.end <= self.end:
            if other.word in self.word:
                return True # it is contained
        if other.start >= self.start and other.start < self.end:
            if len(other.word) <= len(self.word):
                return True # keep the longest word if they overlapse
        if other.end > self.start and other.end <= self.end:
            if len(other.word) <= len(self.word):
                return True
        return False
    
    def __repr__(self):
        return "'" + self.word + "' (Start:"+str(self.start)+", End:"+str(self.end)+")"
    
def evaluatePasswordDictionary(password):

    with open('english.txt', 'r') as f:
        data = f.read()
        words = set(data.split('\n'))
    for word in words:
        word.lower()
    words.remove('')
        
    words_found = set()
    for word in words:
        if word in password.lower():
            newWord = WordFound(word, password.lower().find(word))
            if word in password: # all are lowercase
                newWord.hasLowercase = True
                newWord.hasUppercase = False
            elif word.upper() in password: # all are uppercase
                newWord.hasLowercase = False
                newWord.hasUppercase = True
            else: # mix of lowercase and uppercase
                newWord.hasLowercase = True
                newWord.hasUppercase = True
            toremove = set()
            for wf in words_found:
                if wf.contains(newWord):
                    toremove.add(newWord)
                elif newWord.contains(wf):
                    toremove.add(wf)
            words_found.add(newWord)
            for word_contained in toremove:
                words_found.remove(word_contained)
    password_without_words = password
    for word_found in words_found:
        password_without_words = password_without_words.replace(word_found.word, "")
                
    passwordHasLowercaseWord = False
    passwordHasUppercaseWord = False
    for word_found in words_found:
        if word_found.hasLowercase:
            passwordHasLowercaseWord = True
        if word_found.hasUppercase:
            passwordHasUppercaseWord = True
    passwordHasLowerUpperWord = passwordHasLowercaseWord and passwordHasUppercaseWord
    allwords = len(words)*passwordHasLowercaseWord + \
                len(words)*passwordHasUppercaseWord + \
                pow(len(words)*passwordHasLowerUpperWord, len(words))
    possible_combinations = pow(allwords, len(words_found))
    
    return password_without_words, possible_combinations

def evaluatePasswordCharacters(password):
    # Checks for the password without the common words, if any
    if password == "":
        return 0
    else: # The password is not only common words (or does not have words at all)
        digit = upper = lower = symbol = False
        for character in password:
            if character.isdigit():
                digit = True
            elif character.isupper():
                upper = True
            elif character.islower():
                lower = True
            else:
                symbol = True
        possible_characters = digit * 10 + upper * 26 + lower * 26 + symbol * 28
        possible_combinations = pow(possible_characters, len(password))
    return possible_combinations
        
def evaluatePassword(password):
    password_without_words, possible_combinations = evaluatePasswordDictionary(password)
    possible_combinations += evaluatePasswordCharacters(password_without_words)
    del password_without_words
    security_bits = round(log(possible_combinations,2),2)
    security_digits = round(log(possible_combinations,10))
    safe = False
    if log(possible_combinations,2) > 64:
        safe = True
    return security_bits, security_digits, safe

if __name__ == '__main__':
    evaluatePasswordDictionary("Rampage2dick*tetest")