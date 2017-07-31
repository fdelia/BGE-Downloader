# http://python-guide-pt-br.readthedocs.io/en/latest/writing/tests/

import unittest
import datetime

from main import build_url
from main import download_data_from_url
from main import save_data

class TestBuildUrl(unittest.TestCase):
    def test_wrong_year_given(self):
        now = datetime.datetime.now()
        year = now.year + 1

        with self.assertRaises(ValueError):
            build_url(1900)
            build_url(year)

    def test_wrong_volume(self):
        with self.assertRaises(ValueError):
            build_url(1997, '0')
            build_url(1997, 'VI')

    # Test is incomplete
    def test_returned_url(self):
        year = datetime.datetime.now().year
        self.assertEqual(build_url(year)[:25], 'http://relevancy.bger.ch/')


class TestDownloadDataFromUrl(unittest.TestCase):
    def test_wrong_url(self):
        with self.assertRaises(ValueError):
            download_data_from_url('foo')

    def test_returned_data_is_correct(self):
        # TODO
        self.skipTest('not sure how data will look yet')
        pass

class SaveData(unittest.TestCase):
    def test_is_file_saved(self):
        filename = 'test_file.csv'
        # TODO
        self.skipTest('how to test if file exists?')
        # remove test_file.csv afterwards




if __name__ == '__main__':
    unittest.main()
