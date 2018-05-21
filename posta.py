#!/usr/bin/python

from datetime import datetime
import argparse
from pprint import pprint
import sys
import requests
import random

sys.exit("NEPOUZIVAT! Pouzitie tohoto pristupu k API nie je pravdepodobne verejne povolene!")

parser = argparse.ArgumentParser(description='Pouzitie API posta.sk na ziskanie info o zasielkach.')
parser.add_argument('--posting_no', required=True, action='store', help='Cislo zasielky - vacsinou zacina "SK..."')
parser.add_argument('--verbose', action='store_true', help='Be verbose')
args = parser.parse_args()

url = "http://api.posta.sk/private/search?q=" + args.posting_no + "&m=tnt"
headers = {
    'Referer': 'http://www.posta.sk/en/sps-embed',
    'Origin': 'http://www.posta.sk',
    'Cache-Control': 'max-age=0',
#    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/' + str(random.randint(100,1000)) + '.' + str(random.randint(0,10)) + '.' + str(random.randint(10,20)) + ' (KHTML, like Gecko) Version/10.0.2 Safari/602.3.12',
    'X-Requested-With': 'XMLHttpRequest',
}
r = requests.get(url, headers=headers)

if args.verbose:
    pprint(r.text)

i = r.json()

if args.verbose:
    pprint(i)

if len(i['parcels']) <= 0:
    sys.exit("Nenajdene zaielky pod tymto oznacenim")

for event in i['parcels'][0]['events']:
    d = event['date']
    dt = datetime(d[0], d[1], d[2], d[3], d[4], d[5])
    print(str(dt) + " " + str(event['desc']['en']))
