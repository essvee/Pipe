import unittest
import googleapiclient
from pipe.harvest.gmail import GmailHarvester


class TestGmailHarvester(unittest.TestCase):

    def test_get_credentials(self):
        harvester = GmailHarvester()
        self.assertTrue(isinstance(harvester.service, googleapiclient.discovery.Resource))


if __name__ == '__main__':
    unittest.main()
