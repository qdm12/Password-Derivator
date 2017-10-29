#!/usr/bin/env python

from unittest import TestCase
try: 
    from unittest.mock import patch, mock_open # Python 3
except ImportError:    
    from mock import patch, mock_open # Python 2.7

from derivatex import passgen


class MasterPasswordDigestException(TestCase):
    def test_init(self):
        with self.assertRaises(passgen.MasterPasswordDigestException):
            raise passgen.MasterPasswordDigestException()     
class Functions(TestCase):
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
    
    @patch('derivatex.passgen.checksumIsValid')
    @patch('derivatex.passgen.isMasterpassworddigestfilePresent')
    def test_read_masterpassworddigest_success(self, mock_isMasterpassworddigestfilePresent, mock_checksumIsValid):
        mock_isMasterpassworddigestfilePresent.return_value = True
        mock_checksumIsValid.return_value = True
        mocked_open = mock_open(read_data=b'digestCSUM')
        with patch('derivatex.passgen.open', mocked_open, create=True):
            password_hash = passgen.read_masterpassworddigest()
        self.assertEqual(password_hash, b'digest')
        
    @patch('derivatex.passgen.checksumIsValid')
    @patch('derivatex.passgen.isMasterpassworddigestfilePresent')
    def test_read_masterpassworddigest_fail_nofile(self, mock_isMasterpassworddigestfilePresent, mock_checksumIsValid):
        mock_isMasterpassworddigestfilePresent.return_value = False
        mock_checksumIsValid.return_value = False
        mocked_open = mock_open(read_data=b'digestCSUM')
        with patch('derivatex.passgen.open', mocked_open, create=True):
            with self.assertRaises(passgen.MasterPasswordDigestException) as context:
                _ = passgen.read_masterpassworddigest()
        self.assertEqual(str(context.exception), "File not found")
                
    @patch('derivatex.passgen.checksumIsValid')
    @patch('derivatex.passgen.isMasterpassworddigestfilePresent')
    def test_read_masterpassworddigest_fail_io(self, mock_isMasterpassworddigestfilePresent, mock_checksumIsValid):
        mock_isMasterpassworddigestfilePresent.return_value = True
        mock_checksumIsValid.return_value = False
        mocked_open = mock_open(read_data=b'digestCSUM')
        mocked_open.side_effect = IOError("File protected")
        with patch('derivatex.passgen.open', mocked_open, create=True):
            with self.assertRaises(passgen.MasterPasswordDigestException) as context:
                _ = passgen.read_masterpassworddigest()
        self.assertEqual(str(context.exception), "File protected")
        
    @patch('derivatex.passgen.checksumIsValid')
    @patch('derivatex.passgen.isMasterpassworddigestfilePresent')
    def test_read_masterpassworddigest_fail_checksum(self, mock_isMasterpassworddigestfilePresent, mock_checksumIsValid):
        mock_isMasterpassworddigestfilePresent.return_value = True
        mock_checksumIsValid.return_value = False
        mocked_open = mock_open(read_data=b'digestCXUM')
        with patch('derivatex.passgen.open', mocked_open, create=True):
            with self.assertRaises(passgen.MasterPasswordDigestException) as context:
                _ = passgen.read_masterpassworddigest()   
        self.assertEqual(str(context.exception), "Checksum error") 

    @patch('derivatex.passgen.Argon2id')
    @patch('derivatex.passgen.sha3')
    def test_intestinize(self, mock_sha3, mock_Argon2id):
        class MockArgon2id:
            def hash(self, password):
                return 'garbagegarbage$digestDIGESTdigestDIGESTdigestDIGESTdigest'
        mock_Argon2id.return_value = MockArgon2id()
        masterpassworddigest = b'masterDiGeSt'
        website_name = b'github'
        digest = passgen.intestinize(masterpassworddigest, website_name)
        self.assertEqual(digest, 'digestDIGESTdigestDIGESTdigest')
        
    @patch('derivatex.passgen.Argon2id')
    @patch('derivatex.passgen.sha3')
    def test_intestinize_nosign(self, mock_sha3, mock_Argon2id):
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
        i = 2
        password = passgen.ensure(characterType, password, i)
        self.assertEqual(password, "Ab0JFDSDFDhg-?KL")
        
    def test_ensure_lowercase(self):
        characterType = "lowercase"
        password = "A0*JFDSDFD68-?KL"
        i = 2
        password = passgen.ensure(characterType, password, i)
        self.assertEqual(password, "A0aJFDSDFD68-?KL")
        
    def test_ensure_uppercase(self):
        characterType = "uppercase"
        password = "0b*786fsh9hg-?-8"
        i = 2
        password = passgen.ensure(characterType, password, i)
        self.assertEqual(password, "0bF786fsh9hg-?-8")

    def test_ensure_symbol(self):
        characterType = "symbol"
        password = "0bA786fsh9hgBCD8"
        i = 2
        password = passgen.ensure(characterType, password, i)
        self.assertEqual(password, "0b>786fsh9hgBCD8")
        
    """
    def test_ensure_characters_rangeInput(self):
        # This relies on test_ensure as it is a relatively simple deterministic function        
        ITER = 1000
        for i in range(ITER):
            print(i)
            password = ''.join(choice(ascii_lowercase) for i in range(10))
            _ = passgen.ensure_characters(password)
    """
    
    def test_ensure_characters_minlen(self):
        # This relies on test_ensure as it is a relatively simple deterministic function        
        password = "abcd"
        password = passgen.ensure_characters(password)
        self.assertEqual(password, 'Bb{1')
        
    def test_ensure_characters_lowercase(self):
        # This relies on test_ensure as it is a relatively simple deterministic function        
        password = "password"
        password = passgen.ensure_characters(password)
        self.assertEqual(password, 'pass0|Bd')
             
    def test_ensure_characters_uppercase(self):
        # This relies on test_ensure as it is a relatively simple deterministic function        
        password = "PASSWORD"
        password = passgen.ensure_characters(password)
        self.assertEqual(password, 'P1!SWaRD')
             
    def test_ensure_characters_digit(self):
        # This relies on test_ensure as it is a relatively simple deterministic function        
        password = "434239043"
        password = passgen.ensure_characters(password)
        self.assertEqual(password, 'B3|23904b')
             
    def test_ensure_characters_symbol(self):
        # This relies on test_ensure as it is a relatively simple deterministic function        
        password = '*$£()*$&*%)*/'
        password = passgen.ensure_characters(password)
        self.assertEqual(password, '*$2b)F$&*%)*/')
        
    def test_ensure_characters_fine(self):
        # This relies on test_ensure as it is a relatively simple deterministic function        
        password = "aaaAAA*0"
        password = passgen.ensure_characters(password)
        self.assertEqual(password, 'aaaAAA*0')
        
    def test_ensure_characters_symbolmissing(self):
        # This relies on test_ensure as it is a relatively simple deterministic function        
        password = "aaaAAA06"
        password = passgen.ensure_characters(password)
        self.assertEqual(password, 'aaaAA>06')
        
    @patch('derivatex.passgen.ensure_characters')
    @patch('derivatex.passgen.intestinize')
    @patch('derivatex.passgen.read_masterpassworddigest')
    def test_passgen(self, mock_read_masterpassworddigest, mock_intestinize, mock_ensure_characters):
        mock_read_masterpassworddigest.return_value = b'digest'
        mock_intestinize.return_value.return_value = "digestDIGESTED"
        mock_ensure_characters.return_value = "digestDIGESTED1*"
        website_name = "test"
        password = passgen.passgen(website_name)
        self.assertEqual(password, "digestDIGESTED1*")
        
        