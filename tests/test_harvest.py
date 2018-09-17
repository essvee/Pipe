import unittest
import googleapiclient
import pipe.src.harvest_gmail as p


class testHarvest(unittest.TestCase):

    def test_get_credentials(self):
        harvest = p.HarvestGmail()
        result = harvest.get_credentials()
        self.assertTrue(isinstance(result, googleapiclient.discovery.Resource))

    def test_constructor(self):
        harvest = p.HarvestGmail()
        self.assertTrue(isinstance(harvest, p.HarvestGmail))


if __name__ == '__main__':
    unittest.main()
