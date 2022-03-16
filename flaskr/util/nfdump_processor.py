#!/usr/bin/env python
import pandas as pd
import pyasn


class Nfdump_processor:

    def __init__(self):
        # DB that converts ip address to Autonomous System numbers.
        # Then, converts those numbers to plaintext names
        self.asn_db = pyasn.pyasn('../../data/as_info/ipasn/ipasn_latest.dat',
                                  '../../data/as_info/as_names/autnames.json')

        time_ranges = ['hour', 'day', 'week']

        curr_data = None

        for range in time_ranges:
            curr_data = pd.read_csv('../../data/nfdump/nfdump_last_'
                                    f'{range}.csv',
                                    engine='pyarrow')

            # Check all destination and source IPs for autonomous BGP names
            curr_data['da'] = curr_data['da'].map(self.get_as_name)
            curr_data['sa'] = curr_data['sa'].map(self.get_as_name)

            # Write over original CSVs
            curr_data.to_csv(f'../../data/nfdump/nfdump_last_{range}.csv',
                             index=False)

    def get_as_name(self, ip):
        # Get autonomous system number of ip address
        asn = self.asn_db.lookup(ip)[0]
        if asn is not None:
            # Append autonomous system name to ip address
            # Remove comma from name to avoid corrupting CSV files
            return ip + ' | ' + self.asn_db.get_as_name(asn).replace(',', '')
        # ip address is not an autnomous system. Return it
        return ip


if __name__ == '__main__':
    Nfdump_processor()
