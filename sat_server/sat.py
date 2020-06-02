#!/usr/bin/python3

#APIs
import json
import os

from sat_modules import utils
from sat_modules import config
from sat_modules import sentinel
from sat_modules import landsat

def download_data(args):

    #Check the format date and if end_date > start_date
    args['inidate'], args['enddate'] = utils.valid_date(args['inidate'], args['enddate'])

    if args['producttype'] == 'S2MSI1C':

        #ESA credentials
        s2_credentials = config.sentinel_pass
        args['username'] = s2_credentials['username']
        args['password'] = s2_credentials['password']

        #download sentinel files
        s = sentinel.download_sentinel(**args)
        s2_tiles = s.download()

        return s2_tiles

    elif args['producttype'] == 'LANDSAT_8_C1':

        #NASA credentials
        l8_credentials = config.landsat_pass
        args['username'] = l8_credentials['username']
        args['password'] = l8_credentials['password']

        #download landsat files
        l = landsat.download_landsat(**args)
        l8_tiles = l.download()

        return l8_tiles
