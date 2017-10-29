from unittest import TestCase

try: 
    from unittest.mock import patch, mock_open # Python 3
except ImportError:    
    from mock import patch, mock_open # Python 2.7
import passgen

class MasterPasswordDigestException(TestCase):
    def test_init(self):
        with self.assertRaises(passgen.MasterPasswordDigestException):
            raise passgen.MasterPasswordDigestException()     
class Functions(TestCase):
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
    
    @patch('passgen.checksumIsValid')
    @patch('passgen.isMasterpassworddigestfilePresent')
    def test_read_masterpassworddigest_success(self, mock_isMasterpassworddigestfilePresent, mock_checksumIsValid):
        mock_isMasterpassworddigestfilePresent.return_value = True
        mock_checksumIsValid.return_value = True
        mocked_open = mock_open(read_data=b'digestCHECKSUM')
        with patch('passgen.open', mocked_open, create=True):
            password_hash = passgen.read_masterpassworddigest()
        self.assertEqual(password_hash, b'digestCHECKSUM')
        
    @patch('passgen.checksumIsValid')
    @patch('passgen.isMasterpassworddigestfilePresent')
    def test_read_masterpassworddigest_fail_nofile(self, mock_isMasterpassworddigestfilePresent, mock_checksumIsValid):
        mock_isMasterpassworddigestfilePresent.return_value = False
        mock_checksumIsValid.return_value = False
        mocked_open = mock_open(read_data=b'digestCHECKSUM')
        with patch('passgen.open', mocked_open, create=True):
            with self.assertRaises(passgen.MasterPasswordDigestException) as context:
                _ = passgen.read_masterpassworddigest()
        self.assertEqual(str(context.exception), "File not found")
                
    @patch('passgen.checksumIsValid')
    @patch('passgen.isMasterpassworddigestfilePresent')
    def test_read_masterpassworddigest_fail_io(self, mock_isMasterpassworddigestfilePresent, mock_checksumIsValid):
        mock_isMasterpassworddigestfilePresent.return_value = True
        mock_checksumIsValid.return_value = False
        mocked_open = mock_open(read_data=b'digestCHECKSUM')
        mocked_open.side_effect = IOError("File protected")
        with patch('passgen.open', mocked_open, create=True):
            with self.assertRaises(passgen.MasterPasswordDigestException) as context:
                _ = passgen.read_masterpassworddigest()
        self.assertEqual(str(context.exception), "File protected")
        
    @patch('passgen.checksumIsValid')
    @patch('passgen.isMasterpassworddigestfilePresent')
    def test_read_masterpassworddigest_fail_checksum(self, mock_isMasterpassworddigestfilePresent, mock_checksumIsValid):
        mock_isMasterpassworddigestfilePresent.return_value = True
        mock_checksumIsValid.return_value = False
        mocked_open = mock_open(read_data=b'digestCHECKSUM')
        with patch('passgen.open', mocked_open, create=True):
            with self.assertRaises(passgen.MasterPasswordDigestException) as context:
                _ = passgen.read_masterpassworddigest()   
        self.assertEqual(str(context.exception), "Checksum error") 

    @patch('passgen.Argon2id')
    def test_intestinize(self, mock_Argon2id):
        class MockArgon2id:
            def hash(self, password):
                return 'garbagegarbage$digestDIGESTdigestDIGESTdigestDIGESTdigest'
        mock_Argon2id.return_value = MockArgon2id()
        masterpassworddigest = b'masterDiGeSt'
        website_name = b'github'
        digest = passgen.intestinize(masterpassworddigest, website_name)
        self.assertEqual(digest, 'digestDIGESTdigestDIGESTdigest')
        
    @patch('passgen.Argon2id')
    def test_intestinize_nosign(self, mock_Argon2id):
        class MockArgon2id:
            def hash(self, password):
                return 'digestDIGESTdigestDIGESTdigestDIGESTdigest'
        mock_Argon2id.return_value = MockArgon2id()
        masterpassworddigest = b'masterDiGeSt'
        website_name = b'github'
        digest = passgen.intestinize(masterpassworddigest, website_name)
        self.assertEqual(digest, 'digestDIGESTdigestDIGESTdigest')
        
    def test_find_characterType(self):
        lowercase = passgen.find_characterType('a')
        uppercase = passgen.find_characterType('A')
        digit = passgen.find_characterType('0')
        symbol = passgen.find_characterType('*')
        self.assertEqual(lowercase, "lowercase")
        self.assertEqual(uppercase, "uppercase")
        self.assertEqual(digit, "digit")
        self.assertEqual(symbol, "symbol")
        
    def test_ensure_digit(self):
        characterType = "digit"
        password = "Ab*JFDSDFDhg-?KL"
        offset = 50
        i = 2
        password = passgen.ensure(characterType, password, offset, i)
        self.assertEqual(password, "Ab5JFDSDFDhg-?KL")
        
    def test_ensure_lowercase(self):
        characterType = "lowercase"
        password = "A0*JFDSDFD68-?KL"
        offset = 50
        i = 2
        password = passgen.ensure(characterType, password, offset, i)
        self.assertEqual(password, "A0sJFDSDFD68-?KL")
        
    def test_ensure_uppercase(self):
        characterType = "uppercase"
        password = "0b*786fsh9hg-?-8"
        offset = 50
        i = 2
        password = passgen.ensure(characterType, password, offset, i)
        self.assertEqual(password, "0bA786fsh9hg-?-8")
        
    def test_ensure_symbol(self):
        characterType = "symbol"
        password = "0bA786fsh9hgBCD8"
        offset = 50
        i = 2
        password = passgen.ensure(characterType, password, offset, i)
        self.assertEqual(password, "0b&786fsh9hgBCD8")
        
    def test_ensure_characters(self): # test more
        #password = "password"
        pass
    
    def test_passgen(self):
        pass