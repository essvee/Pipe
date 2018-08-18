import unittest
import googleapiclient
import pipe.src.gapi


class MyTestCase(unittest.TestCase):

    def test_constructor(self):
        myGapi = pipe.src.gapi.Gapi()
        self.assertTrue(isinstance(myGapi, pipe.src.gapi.Gapi))

    def test_fields(self):
        myGapi = pipe.src.gapi.Gapi()
        result = myGapi.get_credentials()
        self.assertTrue(isinstance(result, googleapiclient.discovery.Resource))



if __name__ == '__main__':
    unittest.main()
