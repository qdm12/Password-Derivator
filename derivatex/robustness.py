from math import log
from derivatex.tools import working_path

class WordFound(object):
    def __init__(self, word, start):
        self.word = word 
        self.start = start
        self.end = self.start + len(word)
        self.hasLowercase = (word != word.upper())
        self.hasUppercase = (word != word.lower())
        # maybe words with symbols, or chinese ?

        if type(self.word) is not str:
            raise Exception("Word is not a string")
        elif len(self.word) == 0:
            raise Exception("Word is empty")
        elif type(self.start) is not int:
            raise Exception("Start is an integer")
        elif self.start < 0:
            raise Exception("Start is an integer")
        
    def contains(self, other):
        if other.start >= self.start and other.end <= self.end:
            return True # it is contained
        if other.start in range(self.start, self.end) and other.end > self.end and len(other.word) <= len(self.word):
            return True # keep the longest word if they overlap
        if other.end in range(self.start+1, self.end+1) and len(other.word) <= len(self.word):
            return True
        else:
            return False
    
    def __repr__(self):
        return "'" + self.word + "' (Start:"+str(self.start)+", End:"+str(self.end)+")"
    
def evaluatePasswordDictionary(password):
    password = str(password) # For python 2.7
    with open(working_path + '\derivatex\english.txt', 'r') as f:
        raw_data = f.read()
    data = raw_data.split('\n')
    dictionary = set()
    average_length = 0
    for w in data:
        w = w.strip()
        average_length += len(w)
        dictionary.add(w)
    average_length /= len(dictionary)
    to_remove = set()
    for word in dictionary:
        if len(word) < 2:
            to_remove.add(word)
    for word in to_remove:
        dictionary.remove(word)
    del to_remove    
    words_found = set()
    for word in dictionary:
        if word.lower() in password.lower():
            start = password.lower().find(word)
            realword = password[start : start + len(word)]
            newWord = WordFound(realword, start)
            words_contained = set()
            for Word in words_found:
                if Word.contains(newWord):
                    words_contained.add(newWord)
                elif newWord.contains(Word):
                    words_contained.add(Word)
            words_found.add(newWord)
            for WordContained in words_contained:
                words_found.remove(WordContained)
    if len(words_found) == 0:
        return password, 0
    password_without_words = password
    for word_found in words_found:
        password_without_words = password_without_words.replace(word_found.word, "")
                
    passwordHasLowercaseWord = False
    passwordHasUppercaseWord = False
    for word_found in words_found:
        passwordHasLowercaseWord = passwordHasLowercaseWord or word_found.hasLowercase
        passwordHasUppercaseWord = passwordHasUppercaseWord or word_found.hasUppercase
    passwordHasLowerUpperWord = passwordHasLowercaseWord and passwordHasUppercaseWord
    passwordHasLowercaseWord = passwordHasLowercaseWord ^ passwordHasLowerUpperWord
    passwordHasUppercaseWord = passwordHasUppercaseWord ^ passwordHasLowerUpperWord
    exponent = 0*passwordHasLowercaseWord + 1*passwordHasUppercaseWord + \
               average_length*passwordHasLowerUpperWord
    allwords = pow(2, exponent) * len(dictionary)
    possible_combinations = int(pow(allwords, len(words_found)))
    
    return password_without_words, possible_combinations

def evaluatePasswordCharacters(password):
    # Checks for the password without the common words, if any
    if password == "":
        possible_combinations = 0
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
    password_without_words, possible_combinations_dict = evaluatePasswordDictionary(password)
    possible_combinations_char = evaluatePasswordCharacters(password_without_words)
    possible_combinations = max(possible_combinations_dict, 1) * max(possible_combinations_char, 1)
    del password_without_words
    security_bits = security_digits = 0
    safe = safer = False
    if possible_combinations > 1:
        security_bits = round(log(possible_combinations,2),2)
        security_digits = round(log(possible_combinations,10))
        if log(possible_combinations,2) > 30:
            safe = True
        if log(possible_combinations,2) > 50:
            safer = True
    return security_bits, security_digits, safe, safer