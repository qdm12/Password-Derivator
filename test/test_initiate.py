#!/usr/bin/env python

from unittest import TestCase
try: 
    from unittest.mock import patch, mock_open # Python 3
except ImportError:    
    from mock import patch, mock_open # Python 2.7

from derivatex import initiate
     
class Functions(TestCase):
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
    
    @patch('derivatex.initiate.time')
    @patch('derivatex.initiate.Argon2id')
    def test_get_time_per_time_cost(self, mock_Argon2id, mock_time):
        mock_time.side_effect = [80.5, 160.5]
        time_per_time_cost = initiate.get_time_per_time_cost()
        mock_Argon2id.assert_called_once_with(time_cost=8)
        self.assertEqual(time_per_time_cost, 10.00)
        

    @patch('derivatex.initiate.evaluatePassword')
    def test_check_master_password_FF(self, mock_evaluatePassword):
        master_password1 = "test"
        master_password2 = "test"
        mock_evaluatePassword.return_value = [10, 3, False, False]
        valid, safer, message = initiate.check_master_password(master_password1, master_password2)
        self.assertFalse(valid, "This should not be valid")
        self.assertFalse(safer, "This should not be safer")
        self.assertEqual(message, "Your password has a security of 10 bits, equivalent to a suitcase lock of 3 digits. This is not safe. Please try again with a more complex password.")
        
    @patch('derivatex.initiate.evaluatePassword')
    def test_check_master_password_TF(self, mock_evaluatePassword):
        master_password1 = "test"
        master_password2 = "test"
        mock_evaluatePassword.return_value = [10, 3, True, False]
        valid, safer, message = initiate.check_master_password(master_password1, master_password2)
        self.assertTrue(valid, "This should be valid")
        self.assertFalse(safer, "This should not be safer")
        self.assertEqual(message, "Your password has a security of 10 bits, equivalent to a suitcase lock of 3 digits. Your password has a weak security. Would you like to enter a more complex password?")
        
    @patch('derivatex.initiate.evaluatePassword')
    def test_check_master_password_TT(self, mock_evaluatePassword):
        master_password1 = "test"
        master_password2 = "test"
        mock_evaluatePassword.return_value = [10, 3, True, True]
        valid, safer, message = initiate.check_master_password(master_password1, master_password2)
        self.assertTrue(valid, "This should be valid")
        self.assertTrue(safer, "This should be safer")
        self.assertEqual(message, "Your password has a security of 10 bits, equivalent to a suitcase lock of 3 digits. Your password is safe, good job.")
        
    @patch('derivatex.initiate.evaluatePassword')
    def test_check_master_password_unmatch(self, mock_evaluatePassword):
        master_password1 = "abc"
        master_password2 = "def"
        mock_evaluatePassword.return_value = [10, 3, True, True]
        valid, safer, message = initiate.check_master_password(master_password1, master_password2)
        self.assertFalse(valid, "This should not be valid")
        self.assertFalse(safer, "This should not be safer")
        self.assertEqual(message, "Passwords do not match. Please try again.")

    def test_get_time_cost(self):
        birthdate = "27/07/1994"
        time_cost = initiate.get_time_cost(birthdate)
        self.assertTrue(80 <= time_cost < 120)
        self.assertEqual(time_cost, 109)
        
    
    @patch('derivatex.initiate.Argon2id')
    @patch('derivatex.initiate.get_time_cost')
    @patch('derivatex.initiate.sha3')
    def test_intestinize(self, mock_sha3, mock_get_time_cost, mock_Argon2id):
        mock_get_time_cost.return_value = 1
        mock_sha3.side_effect = ['', b'BLABLAWXYZ']
        class MockArgon2id:
            def hash(self, password):
                return 'garbagegarbage$digest'
        mock_Argon2id.return_value = MockArgon2id()
        password = b'password'
        birthdate = "27/07/1994"
        digest = initiate.intestinize(password, birthdate)
        self.assertEqual(digest, b'digestWXYZ')
        
    @patch('derivatex.initiate.sha3')
    def test_checksumIsValid_T(self, mock_sha3):
        mock_sha3.return_value = b'WXYZ'
        valid = initiate.checksumIsValid(b'digestWXYZ')
        self.assertTrue(valid, "This checksum is valid")
       
    @patch('derivatex.initiate.sha3') 
    def test_checksumIsValid_F(self, mock_sha3):
        mock_sha3.return_value = b'WXYZ'
        valid = initiate.checksumIsValid(b'digestWBYZ')
        self.assertFalse(valid, "This checksum is not valid")
    
    @patch('derivatex.initiate.sha3')
    def test_checksumIsValid_notBytes(self, mock_sha3):
        mock_sha3.return_value = b'WXYZ'
        valid = initiate.checksumIsValid(10)
        self.assertEqual(valid, False, "This checksum is not of bytes type")

    @patch('derivatex.initiate.intestinize')
    @patch('derivatex.initiate.sha3')
    def test_setup(self, mock_sha3, mock_intestinize):
        master_password = "password"
        birthdate = "17/07/1994"
        mock_intestinize.return_value = b'digestWXYZ'
        with patch('derivatex.initiate.open', mock_open(), create=True) as mockOpen:
            success, message = initiate.setup(master_password, birthdate)
        mockOpen.assert_called_once()
        self.assertTrue(success)
        self.assertEqual(message, "The digest file has been saved. You can now use PassGen.")
        
    @patch('derivatex.initiate.intestinize')
    @patch('derivatex.initiate.sha3')
    def test_setup_fail(self, mock_sha3, mock_intestinize):
        master_password = "password"
        birthdate = "17/07/1994"
        mock_intestinize.return_value = b'digestWXYZ'
        with patch('derivatex.initiate.open', mock_open(), create=True) as mockOpen:
            mockOpen.side_effect=IOError("File not found")
            success, message = initiate.setup(master_password, birthdate)
        mockOpen.assert_called_once()
        self.assertFalse(success)
        self.assertEqual(message, "File writing error (File not found)")
        
        
        
        