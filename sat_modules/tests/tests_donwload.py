#import APIs
import datetime
import os

from sat_modules import sentinel
from sat_modules import landsat

def test_download():

    sd = '2019-06-01'
    ed = '2019-06-10'
    sd = datetime.datetime.strptime(sd, "%Y-%m-%d")
    ed = datetime.datetime.strptime(ed, "%Y-%m-%d")

    s2_args = {'inidate': sd.strftime('%Y-%m-%dT%H:%M:%SZ'),
               'enddate': ed.strftime('%Y-%m-%dT%H:%M:%SZ'),
               'region':' CdP',
               'coordinates': {"W":-2.83 ,"S":41.82,"E":-2.67,"N":41.90},
               'platform': 'Sentinel-2',
               'producttype': 'S2MSI1C',
               'cloud': 80,
               'username': "lifewatch",
               'password': "xdc_lfw_data",
               'output_path': "/home/dani/git/sat/data"}

    s2 = sentinel.download_sentinel(**s2_args)
    s2_tiles = s2.download()

    for tile in s2_tiles:

        tile_path = os.path.join(s2_args['output_path'], '{}.zip'.format(tile))
        print ('{}: {}'.format(tile_path, os.path.isfile(tile_path)))

    l8_args = {'inidate': sd.strftime('%Y-%m-%dT%H:%M:%SZ'),
               'enddate': ed.strftime('%Y-%m-%dT%H:%M:%SZ'),
               'region': 'CdP',
               'coordinates': {"W":-2.83 ,"S":41.82,"E":-2.67,"N":41.90},
               'producttype': 'LANDSAT_8_C1',
               'cloud': 80,
               'username': 'lifewatch',
               'password': 'xdc_lfw_data2018',
               'output_path': '/home/dani/git/sat/data'}

    #download landsat files
    l8 = landsat.download_landsat(**l8_args)
    l8_tiles = l8.download()

    for tile in l8_tiles:

        tile_path = os.path.join(s2_args['output_path'], '{}.tgz'.format(tile))
        print ('{}: {}'.format(tile_path, os.path.isfile(tile_path)))

test_download()
