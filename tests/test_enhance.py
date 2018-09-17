import unittest

from pipe.src.dimensions import Dimensions
from pipe.src.unpaywall import Unpaywall


class TestEnhance(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestEnhance, self).__init__(*args, **kwargs)
        self.dimensions = Dimensions(['10.1080/09397140.2014.944428'])
        self.unpaywall = Unpaywall([['10.1016/j.gecco.2018.e00433']])

    def test_dimensions(self):
        expected = 2.16
        sql, results = self.dimensions.get_citations()
        self.assertEqual(results[0][3], expected)

    def test_unpaywall(self):
        expected = True
        sql, results = self.unpaywall.get_access_data()
        self.assertEqual(results[0][4], expected)


if __name__ == '__main__':
    unittest.main()
