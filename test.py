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
            build_index_url(1997, 'IIII')
            build_index_url(1997, 'VI')

    def test_returned_url(self):
        year = datetime.datetime.now().year
        for vol in ['I', 'II', 'III', 'IV', 'V']:
            self.assertTrue(build_index_url(year, vol).startswith('http://relevancy.bger.ch/php/clir/http/index_atf.php'))


# Test depends on external API! (no mocking)
class TestGetBGEUrlsFromIndex(unittest.TestCase):
    def test_no_valid_url_given(self):
        with self.assertRaises(ValueError):
            get_bge_urls_from_index('ftp://foo.com')

    def test_index_empty(self):
        year = datetime.datetime.now().year
        index_url = build_index_url(year, 'I')
        bge_urls = get_bge_urls_from_index(index_url)
        # Returned list is list and should be empty
        self.assertIsInstance(bge_urls, list)
        self.assertFalse(bge_urls)

    def test_if_url(self):
        year = datetime.datetime.now().year
        index_url = build_index_url(year, 'I')
        bge_urls = get_bge_urls_from_index(index_url)

        if (type(bge_urls) == list and len(bge_urls) > 0):
            for url in bge_urls:
                self.assertTrue(url.startswith('http://relevancy.bger.ch/php/clir/http/index.php'))
        else:
            # Returned list is list and should be empty
            self.assertIsInstance(bge_urls, list)
            self.assertFalse(bge_urls)


# Test depends on external API! (no mocking)
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
