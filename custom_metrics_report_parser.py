#!/usr/bin/env python

import argparse
import csv

parser = argparse.ArgumentParser(description='SignalFx - Custom Metrics Report Parser')
parser.add_argument('-c', '--category', help='1 (Host), 2 (Container), 3 (Custom), 4 (Hi-Res), 5 (Bundled)', default='3')
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

total = 0

metrics_list = {}

print "{:<80} {: >20}".format("\nSignalFx Metric (" + type + ")", "MTS")
print "{:<80} {: >20}".format("---------------------------------------------", "-----")

with open(args['report']) as f:
    reader = csv.DictReader(f, delimiter='\t')
    for row in reader:
        if int(row[type]) != 0:
            total = total + int(row[type])
            metrics_list[row['Metric Name']] = int(row[type])

res = sorted(metrics_list.items(), key=lambda (k,v): v, reverse=True)
for r in res:
    print "{:<80} {: >20}".format(r[0], r[1])

print "{:<80} {: >20}".format("---------------------------------------------", "-----")
print "{:<80} {: >20}".format("Total MTS", total)
