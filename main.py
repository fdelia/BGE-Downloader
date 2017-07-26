import sys
import argparse

import datetime
import requests
import json
from bs4 import BeautifulSoup


# Configs
hdr = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       # 'Accept-Charset': 'de-DE,de;q=0.8,en-US;q=0.6,en;q=0.4,id;q=0.2,nl;q=0.2',
       'Accept-Encoding': 'none',
       'Accept-Language': 'de-DE,de;q=0.8,en-US;q=0.6,en;q=0.4,id;q=0.2,nl;q=0.2',
       'Connection': 'keep-alive'}


#site = BeautifulSoup(urllib2.urlopen("http://www.20min.ch", timeout=10), "html.parser")

def build_url(year, volume='I'):
    """
    """
    year = int(year)
    now = datetime.datetime.now()
    if year < 1954 or year > now.year:
        raise ValueError('Year must be >= 1954 and <= current year.')

    # 2017 = 143
    year_nr = (year - 1954) + 80
    return 'http://relevancy.bger.ch/php/clir/http/index_atf.php?year={}&volume={}&lang=de&zoom=&system=clir'.format(year_nr, volume)


def download_data_from_url(url):
    """
    """
    data = [] # rows
    return data


def save_data(data, filename):
    """
    """
    pass


def main(argv):
    # Argument parser
    parser = argparse.ArgumentParser('Downloads court decision from the Swiss Federal Court and packs them into a csv-file.')
    parser.add_argument('--all', action='store_true', help='downloads all decisions, overwrites other download parameters')
    parser.add_argument('-y', '--year', action='store', help='downloads given year')
    # TODO
    # parser.add_argument('-f', '--file', action='store', help='load file before downloading')
    parser.add_argument('-v', '--volume', action='store', help='downloads given volume (default: all)')
    parser.add_argument('-o', '--output', action='store', default='output.csv', help='save as filename')
    args = parser.parse_args()


    # Treat parameters
    print(args)
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
        years = range(1954, datetime.datetime.now().year + 1)

    if args.volume:
        volumes = [args.volume]
    else:
        volumes = ['I', 'II', 'III', 'IV', 'V']


    # Get data
    data = []
    for year in years:
        for vol in volumes:
            url = build_url(year, vol)
            data += download_data_from_url(url)


    # Save data
    save_data(data, args.output)


if __name__ == "__main__":
    main(sys.argv[1:])
