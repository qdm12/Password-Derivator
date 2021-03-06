#!/usr/bin/env python

import unittest
try: 
    from unittest.mock import patch, mock_open # Python 3
except ImportError:    
    from mock import patch, mock_open # Python 2.7

from derivatex import robustness        
class WordFound(unittest.TestCase):
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
    
    def test_init_startend(self):
        word = "quentin"
        start = 2
        w = robustness.WordFound(word, start)
        self.assertEqual(w.word, "quentin", "Word stored incorrectly")
        self.assertTrue(w.hasLowercase, "Lowercase detection is wrong")
        self.assertFalse(w.hasUppercase, "Uppercase detection is wrong")
        self.assertEqual(w.start, 2, "Start index is wrong")
        self.assertEqual(w.end, 9, "End index is wrong")
    
    def test_init_uppercase(self):
        word = "QUENTIN"
        start = 2
        w = robustness.WordFound(word, start)
        self.assertEqual(w.word, "QUENTIN", "Word stored incorrectly")
        self.assertFalse(w.hasLowercase, "Lowercase detection is wrong")
        self.assertTrue(w.hasUppercase, "Uppercase detection is wrong")
        self.assertEqual(w.start, 2, "Start index is wrong")
        self.assertEqual(w.end, 9, "End index is wrong")
        
    def test_init_mixedcase(self):
        word = "QuENTIN"
        start = 2
        w = robustness.WordFound(word, start)
        self.assertEqual(w.word, "QuENTIN", "Word stored incorrectly")
        self.assertTrue(w.hasLowercase, "Lowercase detection is wrong")
        self.assertTrue(w.hasUppercase, "Uppercase detection is wrong")
        self.assertEqual(w.start, 2, "Start index is wrong")
        self.assertEqual(w.end, 9, "End index is wrong")
    
    def test_init_wordtype(self):
        word = 21
        start = 2
        with self.assertRaises(Exception):
            robustness.WordFound(word, start)
        
    def test_init_wordempty(self):
        word = ""
        start = 2
        with self.assertRaises(Exception):
            robustness.WordFound(word, start)
        
    def test_init_starttype(self):
        word = "quentin"
        start = "xx"
        with self.assertRaises(Exception):
            robustness.WordFound(word, start)
        
    def test_init_startnegative(self):
        word = "quentin"
        start = -2
        with self.assertRaises(Exception):
            robustness.WordFound(word, start)
        
    def test_contains_contain(self):
        word1 = "xxxxxxx"
        start1 = 2
        word2 = "xxx"
        start2 = 5
        w1 = robustness.WordFound(word1, start1)
        w2 = robustness.WordFound(word2, start2)
        result = w1.contains(w2)
        self.assertTrue(result, "Word 2 is contained in word 1 but this was not detected")
        
    def test_contains_notcontain(self):
        word1 = "xxxxxxx"
        start1 = 2
        word2 = "xxx"
        start2 = 11
        w1 = robustness.WordFound(word1, start1)
        w2 = robustness.WordFound(word2, start2)
        result = w1.contains(w2)
        self.assertFalse(result, "Word 2 is not contained in word 1 but this was not detected")

    def test_contains_overlap_longer_after(self):
        word1 = "xxxxxxx"
        start1 = 0
        word2 = "xxxxxxxxxx"
        start2 = 2
        w1 = robustness.WordFound(word1, start1)
        w2 = robustness.WordFound(word2, start2)
        result = w1.contains(w2)
        self.assertFalse(result)
        
    def test_contains_overlap_longer_before(self):
        word1 = "xxxxxxx"
        start1 = 2
        word2 = "xxxxxxxxxx"
        start2 = 0
        w1 = robustness.WordFound(word1, start1)
        w2 = robustness.WordFound(word2, start2)
        result = w1.contains(w2)
        self.assertFalse(result)
        
    def test_contains_overlap_shorter_after(self):
        word1 = "xxxxxxxxxx"
        start1 = 0
        word2 = "xxxxxxx"
        start2 = 2
        w1 = robustness.WordFound(word1, start1)
        w2 = robustness.WordFound(word2, start2)
        result = w1.contains(w2)
        self.assertTrue(result)

    def test_contains_overlap_shorter_before(self):
        word1 = "xxxxxxxxxx"
        start1 = 2
        word2 = "xxxxxxx"
        start2 = 0
        w1 = robustness.WordFound(word1, start1)
        w2 = robustness.WordFound(word2, start2)
        result = w1.contains(w2)
        self.assertTrue(result)
            
    def test_contains_overlap_same_after(self):
        word1 = "xxxxxxx"
        start1 = 0
        word2 = "xxxxxxx"
        start2 = 2
        w1 = robustness.WordFound(word1, start1)
        w2 = robustness.WordFound(word2, start2)
        result = w1.contains(w2)
        self.assertTrue(result)
        
    def test_contains_overlap_same_before(self):
        word1 = "xxxxxxx"
        start1 = 2
        word2 = "xxxxxxx"
        start2 = 0
        w1 = robustness.WordFound(word1, start1)
        w2 = robustness.WordFound(word2, start2)
        result = w1.contains(w2)
        self.assertTrue(result)
        
    def test_repr(self):
        word = "quenTin"
        start = 2
        w = robustness.WordFound(word, start)
        result = str(w)
        self.assertEqual(result, "'quenTin' (Start:2, End:9)", "Representation does not match what was there before")
        
class Functions(unittest.TestCase):
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
    
    def test_evaluatePasswordDictionary_empty(self):
        password = ""
        mocked_open = mock_open(read_data='abc \n def \n hij \n klm \n opq')
        with patch('derivatex.robustness.open', mocked_open, create=True):
            password_without_words, possible_combinations = robustness.evaluatePasswordDictionary(password)
        self.assertEqual(password_without_words, "", "Word was not removed from password")
        self.assertEqual(possible_combinations, 0, "Number of combinations is wrong")

    def test_evaluatePasswordDictionary_lowercase(self):
        password = "z2defvbhabchd1l**c"
        mocked_open = mock_open(read_data='abc \n def \n hij \n klm \n opq')
        with patch('derivatex.robustness.open', mocked_open, create=True):
            password_without_words, possible_combinations = robustness.evaluatePasswordDictionary(password)
        self.assertEqual(password_without_words, "z2vbhhd1l**c", "Word was not removed from password")
        self.assertEqual(possible_combinations, pow(5, 2), "Number of combinations is wrong")
        
    def test_evaluatePasswordDictionary_uppercase(self):
        password = "z2DEFvbhABChd1l**c"
        mocked_open = mock_open(read_data='abc \n def \n hij \n klm \n opq')
        with patch('derivatex.robustness.open', mocked_open, create=True):
            password_without_words, possible_combinations = robustness.evaluatePasswordDictionary(password)
        self.assertEqual(password_without_words, "z2vbhhd1l**c", "Word was not removed from password")
        self.assertEqual(possible_combinations, pow(10, 2), "Number of combinations is wrong")
        
    def test_evaluatePasswordDictionary_mixedcase(self):
        password = "z2DeFvbhABChd1l**c"
        mocked_open = mock_open(read_data='abc \n def \n hij \n klm \n opq')
        with patch('derivatex.robustness.open', mocked_open, create=True):
            password_without_words, possible_combinations = robustness.evaluatePasswordDictionary(password)
        self.assertEqual(password_without_words, "z2vbhhd1l**c", "Word was not removed from password")
        self.assertEqual(possible_combinations, pow(pow(2,3) * 5, 2), "Number of combinations is wrong")
        
        
    def test_evaluatePasswordDictionary_overlap1(self):
        password = "abcdefghiii"
        mocked_open = mock_open(read_data='abcdefghi \n def \n hij \n klm \n opq')
        with patch('derivatex.robustness.open', mocked_open, create=True):
            password_without_words, possible_combinations = robustness.evaluatePasswordDictionary(password)
        self.assertEqual(password_without_words, "ii", "Word was not removed from password")
        self.assertEqual(possible_combinations, pow(5, 1), "Number of combinations is wrong")
        
    def test_evaluatePasswordDictionary_overlap2(self):
        password = "abcdefghiii"
        mocked_open = mock_open(read_data='abc \n def \n abcdefghi \n klm \n opq')
        with patch('derivatex.robustness.open', mocked_open, create=True):
            password_without_words, possible_combinations = robustness.evaluatePasswordDictionary(password)
        self.assertEqual(password_without_words, "ii", "Word was not removed from password")
        self.assertEqual(possible_combinations, pow(5, 1), "Number of combinations is wrong")
        
    def test_evaluatePasswordDictionary_badword(self):
        password = "abcddd"
        mocked_open = mock_open(read_data='abc \n def \n abcdefghi \n klm \n opq \n')
        with patch('derivatex.robustness.open', mocked_open, create=True):
            password_without_words, possible_combinations = robustness.evaluatePasswordDictionary(password)
        self.assertEqual(password_without_words, "ddd", "Word was not removed from password")
        self.assertEqual(possible_combinations, pow(5,1), "Number of combinations is wrong")
        
    def test_evaluatePasswordDictionary_nowords(self):
        password = "xxxxxxx"
        mocked_open = mock_open(read_data='abc \n def \n abcdefghi \n klm \n opq \n')
        with patch('derivatex.robustness.open', mocked_open, create=True):
            password_without_words, possible_combinations = robustness.evaluatePasswordDictionary(password)
        self.assertEqual(password_without_words, "xxxxxxx", "Word was not removed from password")
        self.assertEqual(possible_combinations, 0, "Number of combinations is wrong")
        
    def test_evaluatePasswordCharacters_empty(self):
        password = ""
        possible_combinations = robustness.evaluatePasswordCharacters(password)
        self.assertEqual(possible_combinations, 0, "Number of combinations is wrong")
        
    def test_evaluatePasswordCharacters_digit(self):
        password = "1211"
        possible_combinations = robustness.evaluatePasswordCharacters(password)
        self.assertEqual(possible_combinations, pow(10,4), "Number of combinations is wrong")
        
    def test_evaluatePasswordCharacters_lowercase(self):
        password = "abc"
        possible_combinations = robustness.evaluatePasswordCharacters(password)
        self.assertEqual(possible_combinations, pow(26,3), "Number of combinations is wrong")
        
    def test_evaluatePasswordCharacters_uppercase(self):
        password = "ABC"
        possible_combinations = robustness.evaluatePasswordCharacters(password)
        self.assertEqual(possible_combinations, pow(26,3), "Number of combinations is wrong")
        
    def test_evaluatePasswordCharacters_symbol(self):
        password = "*?@"
        possible_combinations = robustness.evaluatePasswordCharacters(password)
        self.assertEqual(possible_combinations, pow(28,3), "Number of combinations is wrong")
        
    def test_evaluatePasswordCharacters_complex(self):
        password = "aB*2z?@"
        possible_combinations = robustness.evaluatePasswordCharacters(password)
        self.assertEqual(possible_combinations, pow(10+26+26+28,7), "Number of combinations is wrong")
        
    def test_evaluatePassword_real(self):
        password = "defaA*00000" # 5^1 * (26+26+28+10)^8 = 21523360500000000
        mocked_open = mock_open(read_data='abc \n def \n abcdefghi \n klm \n opq')
        with patch('derivatex.robustness.open', mocked_open, create=True):
            security_bits, security_digits, safe, safer = robustness.evaluatePassword(password)
        self.assertEqual(security_bits, 54.26, "Security bits is wrong")
        self.assertEqual(security_digits, 16, "Security digits is wrong")
        self.assertTrue(safe, "This has 54.26 bits of security and should be safe")
        self.assertTrue(safer, "This has 54.26 bits of security and should be safer")
        
    @patch('derivatex.robustness.evaluatePasswordCharacters')
    @patch('derivatex.robustness.evaluatePasswordDictionary')
    def test_evaluatePassword_success(self, mock_evaluatePasswordDictionary, mock_evaluatePasswordCharacters):
        password = "test"
        mock_evaluatePasswordDictionary.return_value = [password, 100000000]
        mock_evaluatePasswordCharacters.return_value = 200000000
        security_bits, security_digits, safe, safer = robustness.evaluatePassword(password)
        self.assertEqual(security_bits, 54.15, "Security bits is wrong")
        self.assertEqual(security_digits, 16, "Security digits is wrong")
        self.assertTrue(safe, "xxxxx")
        self.assertTrue(safer, "xxxxx")
 
    @patch('derivatex.robustness.evaluatePasswordCharacters')
    @patch('derivatex.robustness.evaluatePasswordDictionary')
    def test_evaluatePassword_fail(self, mock_evaluatePasswordDictionary, mock_evaluatePasswordCharacters):
        password = "test"
        mock_evaluatePasswordDictionary.return_value = [password, 10]
        mock_evaluatePasswordCharacters.return_value = 50
        security_bits, security_digits, safe, safer = robustness.evaluatePassword(password)
        self.assertEqual(security_bits, 8.97, "Security bits is wrong")
        self.assertEqual(security_digits, 3, "Security digits is wrong")
        self.assertFalse(safe, "This should not be safe")
        self.assertFalse(safer, "This should not be safe or safer")
         
    @patch('derivatex.robustness.evaluatePasswordCharacters')
    @patch('derivatex.robustness.evaluatePasswordDictionary')
    def test_evaluatePassword_fail_empty(self, mock_evaluatePasswordDictionary, mock_evaluatePasswordCharacters):
        password = ""
        mock_evaluatePasswordDictionary.return_value = [password, 0]
        mock_evaluatePasswordCharacters.return_value = 0
        security_bits, security_digits, safe, safer = robustness.evaluatePassword(password)
        self.assertEqual(security_bits, 0, "Security bits is wrong")
        self.assertEqual(security_digits, 0, "Security digits is wrong")
        self.assertFalse(safe, "This an empty password and is not safe")
        self.assertFalse(safer, "This an empty password and is not safer")
        

if __name__ == "__main__":
    unittest.main()
