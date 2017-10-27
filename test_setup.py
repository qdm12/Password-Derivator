from unittest import TestCase
from unittest.mock import patch, mock_open
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
    def test_intestinize(self, mock_get_time_cost, mock_Argon2id):
        mock_get_time_cost.return_value = 1
        class MockArgon2id:
            def hash(self, password):
                return 'garbagegarbage$digest'
        mock_Argon2id.return_value = MockArgon2id()
        password = b'password'
        birthdate = "27/07/1994"
        digest = setup.intestinize(password, birthdate)
        self.assertEqual(digest, b'digest\xe6z\x0c\xc6')
        
    def test_checksumIsValid_T(self):
        valid = setup.checksumIsValid(b'digest\xe6z\x0c\xc6')
        self.assertEqual(valid, True, "This checksum is a valid SHA3-256 checksum")
        
    def test_checksumIsValid_F(self):
        valid = setup.checksumIsValid(b'dygest\xe6z\x0c\xc6')
        self.assertEqual(valid, False, "This checksum is not a valid SHA3-256 checksum")
        
    def test_checksumIsValid_notBytes(self):
        valid = setup.checksumIsValid('digest\xe6z\x0c\xc6')
        self.assertEqual(valid, False, "This checksum is not of bytes type")

    @patch('setup.intestinize')
    def test_setup(self, mock_intestinize):
        master_password = "password"
        birthdate = "17/07/1994"
        mock_intestinize.return_value = b'digestCHECKSUM'
        with patch('setup.open', mock_open(), create=True) as mockOpen:
            success, message = setup.setup(master_password, birthdate)
        mockOpen.assert_called_once()
        self.assertTrue(success)
        self.assertEqual(message, "The digest file has been saved. You can now use PassGen.")
        
    @patch('setup.intestinize')
    def test_setup_fail(self, mock_intestinize):
        master_password = "password"
        birthdate = "17/07/1994"
        mock_intestinize.return_value = b'digestCHECKSUM'
        with patch('setup.open', mock_open(), create=True) as mockOpen:
            mockOpen.side_effect=IOError("File not found")
            success, message = setup.setup(master_password, birthdate)
        mockOpen.assert_called_once()
        self.assertFalse(success)
        self.assertEqual(message, "File writing error (File not found)")
        
        
        
        