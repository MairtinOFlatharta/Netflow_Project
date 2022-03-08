from flask_user import UserMixin
import pandas as pd
from mongoengine import Document, BooleanField, StringField, ListField


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
        # TODO: Should be using pyarrow engine but returns ValueError
        self.data = pd.read_csv(f'data/nfdump/nfdump_last_{time_range}.csv',
                                engine='c')
        self.time_range = time_range

    def get_dst_addr_traffic(self):
        # Get total in and out bytes by destination address
        res = self.data.groupby(['da']).sum().get(['ibyt', 'obyt'])
        return res.to_json()

    def get_dst_port_traffic(self):
        # Get total in and out bytes by destination port
        res = self.data.groupby(['dp', 'pr']).sum().get(['ibyt', 'obyt'])
        return res.to_json()

    def get_src_addr_traffic(self):
        # Get total in and out bytes by source address
        res = self.data.groupby(['sa']).sum().get(['ibyt', 'obyt'])
        return res.to_json()

    def get_src_port_traffic(self):
        # Get total in and out bytes by source port
        res = self.data.groupby(['sp','pr']).sum().get(['ibyt', 'obyt'])
        return res.to_json()

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
