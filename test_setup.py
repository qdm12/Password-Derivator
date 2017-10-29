from unittest import TestCase
try: 
    from unittest.mock import patch, mock_open # Python 3
except ImportError:    
    from mock import patch, mock_open # Python 2.7

import setup
     
class Functions(TestCase):
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
    
    @patch('setup.time')
    @patch('setup.Argon2id')
    def test_get_time_per_time_cost(self, mock_Argon2id, mock_time):
        mock_time.side_effect = [80.5, 160.5]
        time_per_time_cost = setup.get_time_per_time_cost()
        mock_Argon2id.assert_called_once_with(time_cost=8)
        self.assertEqual(time_per_time_cost, 10.00)
        

    @patch('setup.evaluatePassword')
    def test_check_master_password_FF(self, mock_evaluatePassword):
        master_password1 = "test"
        master_password2 = "test"
        mock_evaluatePassword.return_value = [10, 3, False, False]
        valid, safer, message = setup.check_master_password(master_password1, master_password2)
        self.assertEqual(valid, False, "This should not be valid")
        self.assertEqual(safer, False, "This should not be safer")
        self.assertEqual(message, "Your password has a security of 10 bits, equivalent to a suitcase lock of 3 digits. This is not safe. Please try again with a more complex password.")
        
    @patch('setup.evaluatePassword')
    def test_check_master_password_TF(self, mock_evaluatePassword):
        master_password1 = "test"
        master_password2 = "test"
        mock_evaluatePassword.return_value = [10, 3, True, False]
        valid, safer, message = setup.check_master_password(master_password1, master_password2)
        self.assertEqual(valid, True, "This should be valid")
        self.assertEqual(safer, False, "This should not be safer")
        self.assertEqual(message, "Your password has a security of 10 bits, equivalent to a suitcase lock of 3 digits. Your password has a weak security. Would you like to enter a more complex password?")
        
    @patch('setup.evaluatePassword')
    def test_check_master_password_TT(self, mock_evaluatePassword):
        master_password1 = "test"
        master_password2 = "test"
        mock_evaluatePassword.return_value = [10, 3, True, True]
        valid, safer, message = setup.check_master_password(master_password1, master_password2)
        self.assertEqual(valid, True, "This should be valid")
        self.assertEqual(safer, True, "This should be safer")
        self.assertEqual(message, "Your password has a security of 10 bits, equivalent to a suitcase lock of 3 digits. Your password is safe, good job.")
        
    @patch('setup.evaluatePassword')
    def test_check_master_password_unmatch(self, mock_evaluatePassword):
        master_password1 = "abc"
        master_password2 = "def"
        mock_evaluatePassword.return_value = [10, 3, True, True]
        valid, safer, message = setup.check_master_password(master_password1, master_password2)
        self.assertEqual(valid, False, "This should not be valid")
        self.assertEqual(safer, False, "This should not be safer")
        self.assertEqual(message, "Passwords do not match. Please try again.")

    def test_get_time_cost(self):
        birthdate = "27/07/1994"
        time_cost = setup.get_time_cost(birthdate)
        self.assertTrue(80 <= time_cost < 120)
        self.assertEqual(time_cost, 108)
        
    
    @patch('setup.Argon2id')
    @patch('setup.get_time_cost')
    @patch('setup.sha3')
    def test_intestinize(self, mock_sha3, mock_get_time_cost, mock_Argon2id):
        mock_get_time_cost.return_value = 1
        mock_sha3.side_effect = ['', b'BLABLAWXYZ']
        class MockArgon2id:
            def hash(self, password):
                return 'garbagegarbage$digest'
        mock_Argon2id.return_value = MockArgon2id()
        password = b'password'
        birthdate = "27/07/1994"
        digest = setup.intestinize(password, birthdate)
        self.assertEqual(digest, b'digestWXYZ')
        
    @patch('setup.sha3')
    def test_checksumIsValid_T(self, mock_sha3):
        mock_sha3.return_value = b'WXYZ'
        valid = setup.checksumIsValid(b'digestWXYZ')
        self.assertEqual(valid, True, "This checksum is valid")
       
    @patch('setup.sha3') 
    def test_checksumIsValid_F(self, mock_sha3):
        mock_sha3.return_value = b'WXYZ'
        valid = setup.checksumIsValid(b'digestWBYZ')
        self.assertEqual(valid, False, "This checksum is not valid")
    
    @patch('setup.sha3')
    def test_checksumIsValid_notBytes(self, mock_sha3):
        mock_sha3.return_value = b'WXYZ'
        valid = setup.checksumIsValid('digestWXYZ')
        self.assertEqual(valid, False, "This checksum is not of bytes type")

    @patch('setup.intestinize')
    @patch('setup.sha3')
    def test_setup(self, mock_sha3, mock_intestinize):
        master_password = "password"
        birthdate = "17/07/1994"
        mock_intestinize.return_value = b'digestWXYZ'
        with patch('setup.open', mock_open(), create=True) as mockOpen:
            success, message = setup.setup(master_password, birthdate)
        mockOpen.assert_called_once()
        self.assertTrue(success)
        self.assertEqual(message, "The digest file has been saved. You can now use PassGen.")
        
    @patch('setup.intestinize')
    @patch('setup.sha3')
    def test_setup_fail(self, mock_sha3, mock_intestinize):
        master_password = "password"
        birthdate = "17/07/1994"
        mock_intestinize.return_value = b'digestWXYZ'
        with patch('setup.open', mock_open(), create=True) as mockOpen:
            mockOpen.side_effect=IOError("File not found")
            success, message = setup.setup(master_password, birthdate)
        mockOpen.assert_called_once()
        self.assertFalse(success)
        self.assertEqual(message, "File writing error (File not found)")
        
        
        
        