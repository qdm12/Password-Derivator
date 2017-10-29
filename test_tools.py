from unittest import TestCase
try: 
    from unittest.mock import patch # Python 3
except ImportError:    
    from mock import patch # Python 2.7
    
import tools


class Functions(TestCase):
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
    
    @patch('tools.isfile')
    def test_isMasterpassworddigestfilePresent_True(self, mock_isfile):
        mock_isfile.return_value = True
        result = tools.isMasterpassworddigestfilePresent()
        self.assertTrue(result)
        
    @patch('tools.isfile')
    def test_isMasterpassworddigestfilePresent_False(self, mock_isfile):
        mock_isfile.return_value = False
        result = tools.isMasterpassworddigestfilePresent()
        self.assertFalse(result)
    
    def test_sha3_bytes(self):
        value = b'bytesbytes'
        digest = tools.sha3(value)
        self.assertEqual(digest, b'\xcb\t\xa2\x8f\x8f\x8c?u\xcef\x97\x1aI\xcbja\xab\xc1\xb8\xcb\x95(\x96u+l\'m\xa7\xb5}"')
        
    def test_sha3_notbytes(self):
        value = 'bytesbytes'
        digest = tools.sha3(value)
        self.assertEqual(digest, b'\xcb\t\xa2\x8f\x8f\x8c?u\xcef\x97\x1aI\xcbja\xab\xc1\xb8\xcb\x95(\x96u+l\'m\xa7\xb5}"')
        
    def test_sha3_empty(self):
        value = ''
        digest = tools.sha3(value)
        self.assertEqual(digest, b'\xa7\xff\xc6\xf8\xbf\x1e\xd7fQ\xc1GV\xa0a\xd6b\xf5\x80\xffM\xe4;I\xfa\x82\xd8\nK\x80\xf8CJ')
        
    def test_sha3_bytes_hexa(self):
        value = b'bytesbytes'
        digest = tools.sha3(value, hexa=True)
        self.assertEqual(digest, 'cb09a28f8f8c3f75ce66971a49cb6a61abc1b8cb952896752b6c276da7b57d22')
        
    def test_sha3_notbytes_hexa(self):
        value = 'bytesbytes'
        digest = tools.sha3(value, hexa=True)
        self.assertEqual(digest, 'cb09a28f8f8c3f75ce66971a49cb6a61abc1b8cb952896752b6c276da7b57d22')