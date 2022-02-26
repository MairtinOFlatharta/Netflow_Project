#!/usr/bin/env bash

# Path to nfcapd packet captures
NFCAPDDIR=/var/cache/nfdump/

# Path to csv storage directory
NFDUMPDIR=../data/nfdump/

# Run nfdump for last hour, day and week. Cut last 3 rows of output. Cut columns 16-48 (always shows 0s) and output to files
nfdump -R $NFCAPDDIR -B -o csv -t -3600 | head -n -3 | cut -d, -f16-48 --complement > $(pwd)/$NFDUMPDIR/nfdump_last_hour.csv
nfdump -R $NFCAPDDIR -B -o csv -t -86400 | head -n -3 | cut -d, -f16-48 --complement > $(pwd)/$NFDUMPDIR/nfdump_last_day.csv
nfdump -R $NFCAPDDIR -B -o csv -t -604800 | head -n -3 | cut -d, -f16-48 --complement > $(pwd)/$NFDUMPDIR/nfdump_last_week.csv
