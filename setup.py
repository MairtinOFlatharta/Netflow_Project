#!/usr/bin/env python
import json
import os
import binascii
import errno
import subprocess


def main():
    print('Running setup for Netflow Monitoring Tool...')

    print('Creating NFDump data directories...')
    data_path = 'data/nfdump/'
    # Make directory for data/nfdump. If it exists, ignore it
    try:
        os.makedirs(data_path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    print('Generating empty NFDump files...')
    data_files = ['nfdump_last_hour.csv', 'nfdump_last_day.csv',
                  'nfdump_last_week.csv']
    for f in data_files:
        # Generate empty CSV files with above names
        with open(os.path.join(data_path, f), 'w+'):
            pass

    print('Creating BGP Autonomous System data directories...')
    asn_path = 'data/as_info/'
    # Make directories for BGP ASN data
    try:
        os.makedirs(asn_path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    try:
        os.makedirs(asn_path + 'as_names/')
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    try:
        os.makedirs(asn_path + 'ipasn/')
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    try:
        os.makedirs(asn_path + 'rib/')
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    key = input('Enter application secret key (Press enter to generate 64 '
                'char hex key): ')
    if key == '':
        # Generate ranndom 64 char hex string
        key = binascii.b2a_hex(os.urandom(64)).decode('utf-8')
    mongo_URI = input('Enter MongoDB connection URI (Press enter to use local '
                      'MongoDB instance): ')
    database = input('Enter database name of MongoDB instance '
                     '(Press enter to use "user" as database): ')
    corporation = input('Enter name of corporation: ')

    config_dict = {
        "SECRET_KEY": key,
        # Set LOCAL_DB based on whether a mongo URI was provided or not
        "LOCAL_DB": mongo_URI == '',
        "MONGODB_SETTINGS": {
            # Set db to user if no database name was given
            "db": 'user' if database == '' else database,
            "host": mongo_URI,
        },
        "USER_APP_NAME": "Netflow Monitoring",
        "USER_COPYRIGHT_YEAR": 2022,
        "USER_CORPORATION_NAME": corporation,
        "USER_ENABLE_EMAIL": False,
        "USER_ENABLE_USERNAME": True,
        "USER_REQUIRE_RETYPE_PASSWORD": False,
        "USER_ENABLE_REGISTER": True,
        "USER_AUTO_LOGIN_AFTER_REGISTER": False,
    }

    print('Writing config to instance/config.json...')
    try:
        os.makedirs('instance/')
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    with open('instance/config.json', 'w+') as f:
        # Dump dictionary to instance/config.json
        json.dump(config_dict, f, indent=4)

    bgp_option = input('Download BGP Autonomous System info? [Y/N]: ')
    if bgp_option.lower() == 'y':
        subprocess.call(['sh', './scripts/get_bgp_data.sh'])
    else:
        print('Skipping BGP data download...')

    print('Setup done!')


if __name__ == '__main__':
    main()
