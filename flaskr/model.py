from flask_user import UserMixin
import pandas as pd
from mongoengine import Document, BooleanField, StringField, ListField
from json import loads


class User(Document, UserMixin):
    active = BooleanField(default=True)

    # User authentication information
    username = StringField(default='')
    password = StringField()

    # User information
    first_name = StringField(default='')
    last_name = StringField(default='')

    # Relationships
    roles = ListField(StringField(), default=[])


class Nfdump_data:

    def __init__(self, time_range):
        if time_range is None:
            # Set data to last hour by default
            time_range = 'hour'
        elif time_range not in ('hour', 'day', 'week'):
            raise ValueError(f"Invalid data time range given!: {time_range}")
        # Read in data from CSV with matching time range
        self.data = pd.read_csv(f'data/nfdump/nfdump_last_{time_range}.csv',
                                engine='pyarrow')
        self.time_range = time_range

    def get_dst_addr_traffic(self):
        # Get top 10 destination addresses based on in_bytes
        top_in = (self.data.groupby(['da']).sum()
                  .sort_values(by='ibyt', ascending=False).head(10))
        # Remove any records where in_bytes = 0
        top_in = top_in[top_in.ibyt != 0].get('ibyt')

        # Get top 10 destination addresses based on out_bytes
        top_out = (self.data.groupby(['da']).sum()
                   .sort_values(by='obyt', ascending=False).head(10))
        # Remove any records where out_bytes = 0
        top_out = top_out[top_out.obyt != 0].get('obyt')
        return (top_in.to_json(), top_out.to_json())

    def get_dst_port_traffic(self):
        # Get top 10 destinations ports based on in_bytes
        top_in = (self.data.groupby(['dp', 'pr']).sum()
                  .sort_values(by='ibyt', ascending=False).head(10))
        # Remove any records where in_bytes = 0
        top_in = top_in[top_in.ibyt != 0].get('ibyt')

        # Get top 10 destination addresses based on out_bytes
        top_out = (self.data.groupby(['dp', 'pr']).sum()
                   .sort_values(by='obyt', ascending=False).head(10))
        # Remove any records where out_bytes = 0
        top_out = top_out[top_out.obyt != 0].get('obyt')
        return (top_in.to_json(), top_out.to_json())

    def get_src_addr_traffic(self):
        # Get top 10 source addresses based on in_bytes
        top_in = (self.data.groupby(['sa']).sum()
                  .sort_values(by='ibyt', ascending=False).head(10))
        # Remove any records where in_bytes = 0
        top_in = top_in[top_in.ibyt != 0].get('ibyt')

        # Get top 10 source addresses based on out_bytes
        top_out = (self.data.groupby(['sa']).sum()
                   .sort_values(by='obyt', ascending=False).head(10))
        # Remove any records where out_bytes = 0
        top_out = top_out[top_out.obyt != 0].get('obyt')
        return (top_in.to_json(), top_out.to_json())

    def get_src_port_traffic(self):
        # Get top 10 source ports based on in_bytes
        top_in = (self.data.groupby(['sp', 'pr']).sum()
                  .sort_values(by='ibyt', ascending=False).head(10))
        # Remove any records where in_bytes = 0
        top_in = top_in[top_in.ibyt != 0].get('ibyt')

        # Get top 10 source ports based on out_bytes
        top_out = (self.data.groupby(['sp', 'pr'])
                   .sum().sort_values(by='obyt', ascending=False).head(10))
        # Remove any records where out_bytes = 0
        top_out = top_out[top_out.obyt != 0].get('obyt')
        return (top_in.to_json(), top_out.to_json())

    def get_longest_connections(self):
        # Get 10 longest connections
        res = self.data.sort_values(['td'], ascending=False).head(10)
        return res

    def get_busiest_connections(self):
        # Get 10 connections with most data transfer (both ways)
        # Use a copy to avoid mutating our actual data
        data_cpy = self.data
        # Get total data transfer of all connections
        data_cpy['byte_sums'] = data_cpy['ibyt'] + data_cpy['obyt']
        res = data_cpy.sort_values(['byte_sums'], ascending=False).head(10)
        return res

    def get_connections_with_matching_port(self, ports):
        res = None
        if ports is None or loads(ports) is None:
            return
        ports = loads(ports)
        for proto, port in ports:
            # For each protocol and port number passed, find all records
            # with matching values
            res = pd.concat([res,
                             self.data.loc[(self.data['pr'] == proto) &
                                           (self.data['dp'] == port)]])
        return res
