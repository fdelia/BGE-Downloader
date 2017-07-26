import time
import urllib2
import json
from bs4 import BeautifulSoup


# Configs
hdr = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       # 'Accept-Charset': 'de-DE,de;q=0.8,en-US;q=0.6,en;q=0.4,id;q=0.2,nl;q=0.2',
       'Accept-Encoding': 'none',
       'Accept-Language': 'de-DE,de;q=0.8,en-US;q=0.6,en;q=0.4,id;q=0.2,nl;q=0.2',
       'Connection': 'keep-alive'}


site = BeautifulSoup(urllib2.urlopen("http://www.20min.ch", timeout=10), "html.parser")


class Downloader():
    pass

def get_urls_from_index(index_url):
    """
    """
    URLs = []
    return URLs

def get_data_from_bge_url(bge_url):
    """
    """
    data = {}
    return data
