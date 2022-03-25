#!/usr/bin/env bash

# Insert CSV headings
echo "ip,manufacturer" > ../data/device_info/arp/arp_details.csv

# Scan all ARP entries and write the IP and the Manufacturer to CSV
arp-scan --localnet | head -n -3 | tail -n +3 | tr -d ',' | tr '\t' ',' | cut -d, -f2 --complement >> ../data/device_info/arp/arp_details.csv

# Append host IP (127.0....) and Manufacturer to CSV
echo "$(hostname -i),$(dmidecode -t system | awk '/Manufacturer/ {$1="";print $0}' | tr -d ' ' | tr ',' ' ')" >> ../data/device_info/arp/arp_details.csv

# Append host IP (192.168....) and Manufacturer to CSV
echo "$(hostname -I | awk '{print $1}'),$(dmidecode -t system | awk '/Manufacturer/ {$1="";print $0}' | tr -d ' ' | tr ',' ' ')" >> ../data/device_info/arp/arp_details.csv
