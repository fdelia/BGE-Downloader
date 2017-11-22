import sys
import argparse

import datetime
import requests
import json
import re
import urllib
# import csv
import numpy as np
from bs4 import BeautifulSoup


# Configs 
# TODO
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       # 'Accept-Charset': 'de-DE,de;q=0.8,en-US;q=0.6,en;q=0.4,id;q=0.2,nl;q=0.2',
       'Accept-Encoding': 'none',
       'Accept-Language': 'de-DE,de;q=0.8,en-US;q=0.6,en;q=0.4,id;q=0.2,nl;q=0.2',
       'Connection': 'keep-alive'}
DEBUG = False
# req = urllib.request.Request(
#     url, 
#     data=None, 
#     headers={
#         'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
#     }
# )
# f = urllib.request.urlopen(req)


# def build_url(year, volume='I'):
#     """
#     """
#     year = int(year)
#     now = datetime.datetime.now()
#     if year < 1954 or year > now.year:
#         raise ValueError('Year must be >= 1954 and <= current year.')

#     # 2017 = 143
#     year_nr = (year - 1954) + 80
#     return 'http://relevancy.bger.ch/php/clir/http/index_atf.php?year={}&volume={}&lang=de&zoom=&system=clir'.format(year_nr, volume)


# def download_data(year, vol):
#     """
#     """
#     url = build_url(year, vol)
#     data = [] # rows

#     html = str(urllib.request.urlopen(url, timeout=10).read())
#     links = re.findall(r'(?<=<a href=")[^"]*', html)
#     for link in links:
#         if "/php/clir/http/index.php?highlight_docid=atf%3A%2F%2" in link:
#             link = link.replace("&amp;", "&")
#             data.append(download_bge('http://relevancy.bger.ch' + link, year, vol))

#     return data

def download_from_list(year, month, day):
    # Give list data into download BGE
    url = 'https://www.bger.ch/ext/eurospider/live/de/php/aza/http/index_aza.php?date={}{:02}{:02}&lang=de&mode=news'.format(year, month, day)
    req = urllib.request.urlopen(url, timeout=10)
    if req.getcode() != 200:
        return False

    soup = BeautifulSoup(req.read(), "html.parser")
    tables = soup.findAll('table')
    if len(tables) < 2:
        return False

    data = []
    for tr in tables[1].findAll('tr')[1:]: # first row is header
        if len(tr.findAll('a')) > 0:
            tds = tr.findAll('td')
            entscheid_datum = tds[1].text
            entscheid_nr = tds[2].text
            url = tds[2].find('a')['href']
            sachgebiet = tds[4].text
        else:
            sachgebiet_desc = tr.text.replace('\n', '')

            data.append(download_bge(url, 
                [str(year), str(month), str(day), entscheid_datum, entscheid_nr, sachgebiet, sachgebiet_desc]))

    return data


def download_bge(url, *args):
    """
    """
    if DEBUG: print(url)
    html = str(urllib.request.urlopen(url, timeout=10).read())
    soup = BeautifulSoup(html, "html.parser")

    bge_name = soup.title.string

    refs_bges = ""; refs_artikel = ""
    if soup.find("div", {"id": "highlight_references"}):
        refs = soup.find("div", {"id": "highlight_references"}).find_all("p")
        for ref in refs:
            if "Artikel" in ref.text:
                refs_artikel = ref.text.replace('   ', '').replace('mehr...', '')
                if DEBUG: print(refs_artikel)

            if "BGE:" in ref.text:
                refs_bges = ref.text.replace('   ', '').replace('mehr...', '')
                if DEBUG: print(refs_bges)

    content = soup.find("div", {"class": "content"}).text

    return args[0] + [content]


def save_data(data, filename):
    """
    """
    # text and other data (eg. references, BGE name)
    f = open(filename, 'a')
    for d in data:
        # print(d)
        row = "','".join(d)
        row = "'" + row + "'"
        f.write(row + '\n')
    f.close()


def main(argv):
    # Argument parser
    parser = argparse.ArgumentParser('Downloads court decision from the Swiss Federal Court and packs them into a csv-file.')
    parser.add_argument('--all', action='store_true', help='downloads all decisions, overwrites other download parameters')
    parser.add_argument('-y', '--year', action='store', help='downloads given year')
    # parser.add_argument('-f', '--from', action='store', help='min year')
    parser.add_argument('-m', '--from_month', action='store', help='start at month (default: 1)', default=1)
    parser.add_argument('-o', '--output', action='store', default='output.csv', help='save as filename')
    args = parser.parse_args()


    # Treat parameters
    if DEBUG: print(args)
    if args.all is False and args.year is None:
        print('No arguments given.\nTo download all use "--all".\nTo download a specific year use "-y".')
        sys.exit(2)

    if args.all is True:
        # Overwrite other parameters
        args.year = None
        args.volume = None

    if args.year is not None:
        years = [args.year]
    else:
        years = range(2000, datetime.datetime.now().year + 1)

    # if args.volume:
    #     volumes = [args.volume]
    # else:
    #     volumes = ['I', 'II', 'III', 'IV', 'V']
    args.from_month = int(args.from_month)
    if args.from_month not in list(range(1, 13)):
        print('Month must be in range from 1 to 12.')
        sys.exit(2)


    # Get data
    #years = [2017]
    for year in years:
        for month in range(args.from_month, 13):
            print('{} {:02}'.format(year, month))
            data = []
            for day in range(1, 32):
                print('    {:02}'.format(day))
                try:
                    d = download_from_list(year, month, day)
                    if d:
                        data += d
                except:
                    print('    Error, passing')
                    pass
                
            print("    {} rows".format(len(data)))

            # Save data
            save_data(data, "data/publ_{}_{}.csv".format(year, month))


if __name__ == "__main__":
    main(sys.argv[1:])
