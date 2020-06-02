#import APIs
import pytest
import argparse

import datetime
import zipfile
import os

from sat_modules import sentinel
from sat_modules import landsat

@pytest.fixture
def download_params():

    sd = '2019-06-01'
    ed = '2019-06-10'
    sd = datetime.datetime.strptime(sd, "%Y-%m-%d")
    ed = datetime.datetime.strptime(ed, "%Y-%m-%d")
    region = "CdP"
    coordinates = {"W":-2.83 ,"S":41.82,"E":-2.67,"N":41.90}
    cloud = 80
    path = '/home/ubuntu/Dani/git/sat/data'

    #Sentinel credentials
    ESA_username = "lifewatch"
    ESA_password = "xdc_lfw_data"

    #NASA credentials
    NASA_username = "lifewatch"
    NASA_password = "xdc_lfw_data2018"

    return [sd, ed, region, coordinates, cloud, path,
            ESA_username, ESA_password, NASA_username, NASA_password]


def test_esa_download(download_params):

    s2_args = {'inidate': download_params[0].strftime('%Y-%m-%dT%H:%M:%SZ'),
               'enddate': download_params[1].strftime('%Y-%m-%dT%H:%M:%SZ'),
               'region': download_params[2],
               'coordinates': download_params[3],
               'platform': 'Sentinel-2',
               'producttype': 'S2MSI1C',
               'cloud': download_params[4],
               'username': download_params[6],
               'password': download_params[7],
               'output_path': os.path.join(download_params[5], "s2_tiles")}

    s2 = sentinel.download_sentinel(**s2_args)
    s2_tiles = s2.download()

    for tile in s2_tiles:

        tile_path = os.path.join(s2_args['output_path'], '{}.zip'.format(tile))
        assert os.path.isfile(tile_path) == True

        # This part of the test only works if you have already downloaded data with the same parameters
        # To verify that the data just downloaded is correct, check the size with the previously downloaded data

        tile_zp = zipfile.ZipFile(tile_path)
        tile_size = sum([zinfo.file_size for zinfo in  tile_zp.filelist])

        downloaded_tile = os.path.join('/home/ubuntu/Dani/git/sat/data', '{}.zip'.format(tile))
        downloaded_zp = zipfile.ZipFile(downloaded_tile)
        downloaded_size = sum([zinfo.file_size for zinfo in  downloaded_zp.filelist])
        assert tile_size == downloaded_size


def test_nasa_search(download_params):

    l8_args = {'inidate': download_params[0].strftime('%Y-%m-%dT%H:%M:%SZ'),
               'enddate': download_params[1].strftime('%Y-%m-%dT%H:%M:%SZ'),
               'region': download_params[2],
               'coordinates': download_params[3],
               'producttype': 'LANDSAT_8_C1',
               'cloud': download_params[4],
               'username': download_params[8],
               'password': download_params[9],
               'output_path': os.path.join(download_params[5], "l8_tiles")}

    #download landsat files
    l8 = landsat.download_landsat(**l8_args)
    l8_tiles = l8.download()

    for tile in l8_tiles:

        tile_path = os.path.join(l8_args['output_path'], '{}.zip'.format(tile))
        assert os.path.isfile(tile_path) == True

        # This part of the test only works if you have already downloaded data with the same parameters
        # To verify that the data just downloaded is correct, check the size with the previously downloaded data

        tile_zp = zipfile.ZipFile(tile_path)
        tile_size = sum([zinfo.file_size for zinfo in  tile_zp.filelist])

        downloaded_tile = os.path.join('/home/ubuntu/Dani/git/sat/data', '{}.zip'.format(tile))
        downloaded_zp = zipfile.ZipFile(downloaded_tile)
        downloaded_size = sum([zinfo.file_size for zinfo in  downloaded_zp.filelist])
        assert tile_size == downloaded_size
