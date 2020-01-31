#!/usr/bin/python3
import argparse
import os

from sat_modules import config
from sat_modules import utils
from sat_modules import sentinel
from sat_modules import landsat

parser = argparse.ArgumentParser(description='Gets data from satellite')

parser.add_argument("-sd",
                    "--startdate",
                    help="The Start Date - format DD-MM-YYYY",
                    required=True,
                    dest='start_date')

parser.add_argument("-ed",
                    "--enddate",
                    help="The Start Date - format DD-MM-YYYY",
                    required=True,
                    dest='end_date')

parser.add_argument("-reg",
                   "--region",
                   help = "Name of the region selected",
                   required=True,
                   choices=['CdP', 'Cogotas', 'Sanabria'])


parser.add_argument('-coord',
                    dest='coord',
                    required=False,
                    help='list of coordinates')

parser.add_argument('--sat',
		    help="Sentinel2 or Landsat8",
		    required=False,
		    choices=['Sentinel2', 'Landsat8', None])

parser.add_argument('--cloud',
            help="Maximum percentage of cloud",
            required=False,)

parser.add_argument('-path',
		   help='output path',
		   required=True)

args = parser.parse_args()

#Check the format date and if end_date > start_date
sd, ed = utils.valid_date(args.start_date, args.end_date)

#chek the region to attach coordinates
coord = utils.valid_region(args.region, args.coord)

if args.sat == "Sentinel2":
    
    #credentials
    s2_credentials = config.sentinel_pass


    S2_args = {'inidate':sd,
               'enddate':ed,
               'region':args.region,
               'coordinates': coord,
               'platform':'Sentinel-2',
               'producttype':'S2MSI1C',
               'cloud': args.cloud,
               'username':s2_credentials['username'],
               'password': s2_credentials['password'],
               'output_path':os.path.join(args.path, 's2_tiles')}

    #download sentinel files
    s = sentinel.download_sentinel(**S2_args)
    s.download()

elif args.sat == "Landsat8":
    
    #credentials
    l8_credentials = config.landsat_pass

    l8_args = {'inidate':sd,
               'enddate':ed,
               'region':args.region,
               'coordinates': coord,
               'producttype':'LANDSAT_8_C1',
               'cloud': args.cloud,
               'username':l8_credentials['username'],
               'password': l8_credentials['password'],
               'output_path':os.path.join(args.path, 'l8_tiles')}

    #download landsat files
    l = landsat.download_landsat(**l8_args)
    l.download()

elif args.sat == None:
    
    #credentials
    s2_credentials = config.sentinel_pass

    S2_args = {'inidate':sd,
               'enddate':ed,
               'region':args.region,
               'coordinates': coord,
               'platform':'Sentinel-2',
               'producttype':'S2MSI1C',
               'cloud': args.cloud,
               'username':s2_credentials['username'],
               'password': s2_credentials['password'],
               'output_path':os.path.join(args.path, 's2_tiles')}

    #download sentinel files
    s = sentinel.download_sentinel(**S2_args)
    s.download()

    #credentials
    l8_credentials = config.landsat_pass

    l8_args = {'inidate':sd,
               'enddate':ed,
               'region':args.region,
               'coordinates': coord,
               'producttype':'LANDSAT_8_C1',
               'cloud': args.cloud,
               'username':l8_credentials['username'],
               'password': l8_credentials['password'],
               'output_path':os.path.join(args.path, 'l8_tiles')}

    #download landsat files
    l = landsat.download_landsat(**l8_args)
    l.download()
