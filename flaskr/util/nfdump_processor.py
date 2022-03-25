#!/usr/bin/env python
import pandas as pd
import pyasn


class Nfdump_processor:

    def __init__(self):
        # DB that converts ip address to Autonomous System numbers.
        # Then, converts those numbers to plaintext names
        self.asn_db = pyasn.pyasn('../../data/as_info/ipasn/ipasn_latest.dat',
                                  '../../data/as_info/as_names/autnames.json')

        self.manufacturers = pd.read_csv('../../data/device_info'
                                         '/arp/arp_details.csv')
        self.hosts = pd.read_csv('../../data/device_info'
                                 '/hosts/known_hosts.csv')

        time_ranges = ['hour', 'day', 'week']

        curr_data = None

        for range in time_ranges:
            curr_data = pd.read_csv('../../data/nfdump/nfdump_last_'
                                    f'{range}.csv',
                                    engine='pyarrow')

            # Check all destination and source IPs for autonomous BGP names
            curr_data['da'] = curr_data['da'].map(self.get_as_name)
            curr_data['sa'] = curr_data['sa'].map(self.get_as_name)

            # Attempt to map private hostnames and manufacturers to sources
            # and destinations
            curr_data['da'] = (curr_data['da']
                               .map(self.get_private_host_and_manufacturer))

            curr_data['sa'] = (curr_data['sa']
                               .map(self.get_private_host_and_manufacturer))

            # Write over original CSVs
            curr_data.to_csv(f'../../data/nfdump/nfdump_last_{range}.csv',
                             index=False)

    def get_as_name(self, ip):
        asn = None
        # Get autonomous system number of ip address
        try:
            asn = self.asn_db.lookup(ip)[0]
        except ValueError:
            # ASN entry was not found. Continue
            pass

        if asn is not None:
            # Append autonomous system name to ip address
            # Remove comma from name to avoid corrupting CSV files
            return ip + ' | ' + self.asn_db.get_as_name(asn).replace(',', '')
        # ip address is not an autnomous system. Return it
        return ip

    def get_private_host_and_manufacturer(self, ip):
        manufacturer = None
        hostname = None

        try:
            # Find private hostname associated with IP address
            hostname = self.hosts.loc[self.hosts['ip'] == ip].iat[0, 1]
        except IndexError:
            # Private hostname for ip wasn't found. Continue
            pass

        try:
            # Find device manufacturer assocaited with IP address in ARP table
            manufacturer = self.manufacturers.loc[
                self.manufacturers['ip'] == ip].iat[0, 1]

        except IndexError:
            # Manufacturer wasn't found. Continue
            pass

        # Append hostname and manufacturer to IP (if they have been found)
        if hostname is None:
            if manufacturer is None:
                return ip
            else:
                return ip + ' | ' + '(' + manufacturer + ')'
        else:
            if manufacturer is None:
                return ip + ' | ' + hostname
            else:
                return ip + ' | ' + hostname + ' (' + manufacturer + ')'

        return ip


if __name__ == '__main__':
    Nfdump_processor()
