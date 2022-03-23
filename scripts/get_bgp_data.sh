#!/usr/bin/env bash

echo "$(date): Running pyasn_util_download.py (downloading AS Numbers)"
pyasn_util_download.py --latest

echo "$(date): Running pyasn_util_convert.py (converting rib file to .dat)"
pyasn_util_convert.py --single ./rib.[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9].*.bz2 ./data/as_info/ipasn/ipasn_latest.dat

# Move rib archive to rib directory
mv ./rib.*.bz2 ./data/as_info/rib/

echo "$(date): Running pyasn_util_asnames.py (getting names of AS Numbers)"
pyasn_util_asnames.py > ./data/as_info/as_names/autnames.json
