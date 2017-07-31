# http://python-guide-pt-br.readthedocs.io/en/latest/writing/tests/

import unittest
import datetime
import re

from main import build_index_url
from main import get_bge_urls_from_index
from main import download_bge_from_url
from main import save_data

class TestIndexBuildUrl(unittest.TestCase):
    def test_wrong_year_given(self):
        now = datetime.datetime.now()
        year = now.year + 1

        with self.assertRaises(ValueError):
            build_index_url(1900, 'I')
            build_index_url(year, 'I')

    def test_wrong_volume_given(self):
        with self.assertRaises(ValueError):
            build_index_url(1997, '0')
            build_index_url(1997, 'VI')

    # Test is incomplete
    def test_returned_url(self):
        year = datetime.datetime.now().year
        self.assertEqual(build_index_url(year)[:25], 'http://relevancy.bger.ch/')

class TestGetBGEUrlsFromIndex(unittest.TestCase):
    def test_no_valid_url_given(self):
        with self.assertRaises(ValueError):
            get_bge_urls_from_index('ftp://foo.com')

    def test_index_empty(self):
        index_url = build_index_url(2007, 'I')
        # Returned list should be empty
        self.assertFalse(get_bge_urls_from_index(index_url))

    def test_if_url(self):
        index_url = build_index_url(2007, 'I')
        bge_urls = get_bge_urls_from_index(index_url)

        for url in bge_urls:
            # matches http://, https://, ftp://
            self.assertTrue(re.match(r'^(?:http|ftp)s?://'))





class TestDownloadBGEFromUrl(unittest.TestCase):
    def test_no_valid_url_given(self):
        with self.assertRaises(ValueError):
            download_bge_from_url('foo')

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
