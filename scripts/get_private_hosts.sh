#!/usr/bin/env bash

# Write column headings
echo "ip,hostname" > ../data/device_info/hosts/known_hosts.csv

# Write known hostnames and corresponding IPs to CSV
cat /etc/hosts | awk '/^1/ {print}' | tr '\t' ',' >> ../data/device_info/hosts/known_hosts.csv

# Append machine hostname and IP address to CSV
echo "$(hostname -I | awk '{print $1}'),$(hostname)" | tr -d ' ' >> ../data/device_info/hosts/known_hosts.csv
