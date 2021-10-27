#!/usr/bin/env python

import argparse
import csv

parser = argparse.ArgumentParser(description='Splunk O11y Cloud - Custom Metrics Report Parser')
parser.add_argument('-c', '--category', help='1 (Host), 2 (Container), 3 (Custom), 4 (Hi-Res), 5 (Bundled)', default='3')
parser.add_argument('-l', '--limit', help='Limit no. of metrics displayed in table', default=10000)
parser.add_argument('-r', '--report', help='Custom Metric Report', required=True)
args = vars(parser.parse_args())

if args['category'] == "1":
    type = 'No. Host MTS'
elif args['category'] == "2":
    type = 'No. Container MTS'
elif args['category'] == "3":
    type = 'No. Custom MTS'
elif args['category'] == "4":
    type = 'No. High Resolution MTS'
elif args['category'] == "5":
    type = 'No. Bundled MTS'

metrics_list = {}

OKGREEN = '\033[92m'
ENDC = '\033[0m'
BOLD = '\033[1m'
    
print(BOLD + OKGREEN + "{: <80} {: >21}".format("\nSplunk Metric (" + type + ")", "MTS") + ENDC)
print(BOLD + OKGREEN + "{: <80} {: >20}".format("-" * 80, "-" * 9) + ENDC)

with open(args['report']) as f:
    reader = csv.DictReader(f, delimiter='\t')
    for row in reader:
        if int(row[type]) != 0:
            metrics_list[row['Metric Name']] = int(row[type])

total = 0
res = sorted(metrics_list.items(), key=lambda v: v[1], reverse=True)
for r in res[:int(args['limit'])]:
    mts = "{:,}".format(r[1])
    print("{: <80} {: >20}".format(r[0], mts))
    total = total + int(r[1])

total = "{:,}".format(total)
print(BOLD + OKGREEN + "{: <80} {: >20}".format("-" * 80, "-" * 9) + ENDC)
print(BOLD + OKGREEN + "{: <80} {: >20}".format("Total MTS", total) + ENDC)
