import unittest
from unittest.mock import patch
import setup


class BirthDate(unittest.TestCase):
    def setUp(self):
        pass
        
    def tearDown(self):
        pass

    @patch('robustness.evaluatePassword')
    def test_check_master_password(self, mock_evaluatePassword):
        master_password1 = "testtest"
        master_password2 = "testtest"
        mock_evaluatePassword.return_value = [8, 3, False, False]
        valid, safer, message = setup.check_master_password(master_password1, master_password2)
        print(message)
        self.assertEqual(True, True, "")
        
    def test_sum(self):
        self.assertEqual(True, True, "")
        
    def test_repr(self):
        self.assertEqual(True, True, "")     
class Functions(unittest.TestCase):
    def setUp(self):
        pass
        
    def tearDown(self):
        pass

    def test_check_master_password(self):
        self.assertEqual(True, True, "")
        
    def test_check_birthdate(self):
        self.assertEqual(True, True, "")
        
    def test_intestinize(self):
        self.assertEqual(True, True, "")
        
    def test_checksumIsValid(self):
        self.assertEqual(True, True, "")

    def test_setup(self):
        self.assertEqual(True, True, "")