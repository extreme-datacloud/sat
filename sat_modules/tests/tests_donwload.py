#import APIs
import datetime
import zipfile
import os

from sat_modules import sentinel
from sat_modules import landsat


def ESA_download(sd, ed, region, coordinates, cloud, credentials, path):

    s2_args = {'inidate': sd.strftime('%Y-%m-%dT%H:%M:%SZ'),
               'enddate': ed.strftime('%Y-%m-%dT%H:%M:%SZ'),
               'region': region,
               'coordinates': coordinates,
               'platform': 'Sentinel-2',
               'producttype': 'S2MSI1C',
               'cloud': cloud,
               'username': credentials["username"],
               'password': credentials["password"],
               'output_path': os.path.join(path, "s2_tiles")}

    s2 = sentinel.download_sentinel(**s2_args)
    s2_tiles = s2.download()

    return s2_tiles


def NASA_download(sd, ed, region, coordinates, cloud, credentials, path):

    l8_args = {'inidate': sd.strftime('%Y-%m-%dT%H:%M:%SZ'),
               'enddate': ed.strftime('%Y-%m-%dT%H:%M:%SZ'),
               'region': region,
               'coordinates': coordinates,
               'producttype': 'LANDSAT_8_C1',
               'cloud': cloud,
               'username': credentials["username"],
               'password': credentials["password"],
               'output_path': os.path.join(path, "l8_tiles")}

    #download landsat files
    l8 = landsat.download_landsat(**l8_args)
    l8_tiles = l8.download()

    return l8_tiles


def test_download():

    sd = '2019-06-01'
    ed = '2019-06-10'
    sd = datetime.datetime.strptime(sd, "%Y-%m-%d")
    ed = datetime.datetime.strptime(ed, "%Y-%m-%d")
    region = "CdP"
    coordinates = {"W":-2.83 ,"S":41.82,"E":-2.67,"N":41.90}
    cloud = 80
    path = '/home/ubuntu/Dani/git/sat/data'

    #Sentinel credentials
    ESA_credentials = {'username':"lifewatch", 'password':"xdc_lfw_data"}
    s2_tiles = ESA_download(sd, ed, region, coordinates, cloud, ESA_credentials, path)

    for tile in s2_tiles:

        tile_path = os.path.join(s2_args['output_path'], '{}.zip'.format(tile))
        assert os.path.isfile(tile_path) == True

        tile_zp = zipfile.ZipFile(tile_path)
        tile_size = sum([zinfo.file_size for zinfo in  zp.filelist])

        downloaded_tile = os.path.join('/home/ubuntu/Dani/git/sat/data', '{}.zip'.format(tile))
        downloaded_zp = zipfile.ZipFile(downloaded_tile)
        downloaded_size = sum([zinfo.file_size for zinfo in  zp.filelist])

        assert tile_size == downloaded_size

    #NASA credentials
    NASA_credentials = {'username':"lifewatch", 'password':"xdc_lfw_data2018"}
    l8_tiles = NASA_download(sd, ed, region, coordinates, cloud, NASA_credentials, path)

    for tile in l8_tiles:

        tile_path = os.path.join(s2_args['output_path'], '{}.tgz'.format(tile))
        assert os.path.isfile(tile_path) == True
