#!/usr/bin/python3
import argparse
import json
import os

from sat_modules import config
from sat_modules import utils
from sat_modules import sentinel
from sat_modules import landsat

parser = argparse.ArgumentParser(description='Gets data from satellite')

parser.add_argument("-sat_args", action="store",
                    required=True, type=str)

parser.add_argument('-path',
                   help='output path',
                   required=True)

args = parser.parse_args()

sat_args = json.loads(args.sat_args)

path = args.path
if not os.path.isdir(path):
    os.mkdir(path)

#Check the format date and if end_date > start_date
sd, ed = utils.valid_date(sat_args['start_date'], sat_args['end_date'])

if sat_args['sat_type'] == "Sentinel2":

    #credentials
    s2_credentials = config.sentinel_pass

    s2_args = {'inidate':sd,
               'enddate':ed,
               'region':sat_args['region'],
               'coordinates':sat_args['coordinates'],
               'platform':'Sentinel-2',
               'producttype':'S2MSI1C',
               'cloud':sat_args['cloud'],
               'username':s2_credentials['username'],
               'password':s2_credentials['password'],
               'output_path':os.path.join(path, 's2_tiles')}

    print ("Downloading Sentinel data")
    print ("Download path: {}".format(s2_args['output_path']))

    #download sentinel files
    s = sentinel.download_sentinel(**s2_args)
    s.download()

elif sat_args['sat_type'] == "Landsat8":

    #credentials
    l8_credentials = config.landsat_pass

    l8_args = {'inidate':sd,
               'enddate':ed,
               'region':sat_args['region'],
               'coordinates':sat_args['coordinates'],
               'producttype':'LANDSAT_8_C1',
               'cloud':sat_args['cloud'],
               'username':l8_credentials['username'],
               'password':l8_credentials['password'],
               'output_path':os.path.join(path, 'l8_tiles')}

    print ("Downloading Landsat data")
    print ("Download path: {}".format(l8_args['output_path']))

    #download landsat files
    l = landsat.download_landsat(**l8_args)
    l.download()

elif sat_args['sat_type'] == 'All':

    #credentials
    s2_credentials = config.sentinel_pass

    s2_args = {'inidate':sd,
               'enddate':ed,
               'region':sat_args['region'],
               'coordinates':sat_args['coordinates'],
               'platform':'Sentinel-2',
               'producttype':'S2MSI1C',
               'cloud':sat_args['cloud'],
               'username':s2_credentials['username'],
               'password':s2_credentials['password'],
               'output_path':os.path.join(path, 's2_tiles')}

    print ("Downloading Sentinel data")
    print ("Download path: {}".format(s2_args['output_path']))

    #download sentinel files
    s = sentinel.download_sentinel(**s2_args)
    s.download()

    #credentials
    l8_credentials = config.landsat_pass

    l8_args = {'inidate':sd,
               'enddate':ed,
               'region':sat_args['region'],
               'coordinates':sat_args['coordinates'],
               'producttype':'LANDSAT_8_C1',
               'cloud':sat_args['cloud'],
               'username':l8_credentials['username'],
               'password':l8_credentials['password'],
               'output_path':os.path.join(path, 'l8_tiles')}

    print ("Downloading Landsat data")
    print ("Download path: {}".format(l8_args['output_path']))

    #download landsat files
    l = landsat.download_landsat(**l8_args)
    l.download()
