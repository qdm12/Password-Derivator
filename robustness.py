from math import log

class WordFound(object):
    def __init__(self, word, start, end):
        self.start = start
        self.end = end
        self.word = word
        
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
        return "WORD: "+self.word+" (Start:"+str(self.start)+", End:"+str(self.end)+")"
    
def evaluatePassword(password):
    # Checks for common words
    with open('english.txt', 'r') as f:
        data = f.read()
        words = set(data.split('\n'))
    words_found = set()
    for word in words:
        if word in password:
            absent = True
            newwf = WordFound(word, password.find(word), password.find(word) + len(word))
            toremove = set()
            for wf in words_found:
                if wf.contains(newwf):
                    absent = False
                if newwf.contains(wf):
                    toremove.add(wf)
            for wf in toremove:
                words_found.remove(wf)
            if absent:
                words_found.add(newwf)
    print(words_found)
    n_words = len(words_found)
    possible_combinations = pow(len(words), n_words)
    password_without_words = password
    for wf in words_found:
        password_without_words = password_without_words.replace(wf.word, "")
    
    # Checks for the password without the common words, if any
    if password_without_words != "":
        # The password is not only common words (or does not have words at all)
        digit = upper = lower = symbol = False
        for character in password_without_words:
            if character.isdigit():
                digit = True
            elif character.isupper():
                upper = True
            elif character.islower():
                lower = True
            else: # Symbol
                symbol = True
        possible_characters = digit * 10 + upper * 26 + lower * 26 + symbol * 28
        possible_combinations += pow(possible_characters, len(password_without_words))
        del possible_characters
    return possible_combinations

def evaluateCombinations(possible_combinations):
    if log(possible_combinations,2) < 16:
        return "Unsafe"
    return "Safe"

if __name__ == '__main__':
    pass