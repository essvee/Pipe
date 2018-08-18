import unittest
import googleapiclient
from pipe.src.gapi import Gapi


class MyTestCase(unittest.TestCase):

    def test_get_credentials(self):
        gapi = Gapi()
        result = gapi.get_credentials()
        self.assertTrue(isinstance(result, googleapiclient.discovery.Resource))



if __name__ == '__main__':
    unittest.main()
