#import APIs
import pytest
import argparse
import datetime
import os

from sat_modules import sentinel
from sat_modules import landsat

@pytest.fixture
def search_params():

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



def test_esa_search(search_params):

    s2_args = {'inidate': search_params[0].strftime('%Y-%m-%dT%H:%M:%SZ'),
               'enddate': search_params[1].strftime('%Y-%m-%dT%H:%M:%SZ'),
               'region': search_params[2],
               'coordinates': search_params[3],
               'platform': 'Sentinel-2',
               'producttype': 'S2MSI1C',
               'cloud': search_params[4],
               'username': search_params[6],
               'password': search_params[7],
               'output_path': os.path.join(search_params[5], "s2_tiles")}

    s2 = sentinel.download_sentinel(**s2_args)
    s2_results = s2.search()

    assert len(s2_results) == 2
    assert s2_results[0]['title'] == 'S2A_MSIL1C_20190608T105621_N0207_R094_T30TWM_20190608T130706'
    assert s2_results[1]['title'] == 'S2B_MSIL1C_20190603T105629_N0207_R094_T30TWM_20190603T131528'


def test_nasa_search(search_params):

    l8_args = {'inidate': search_params[0].strftime('%Y-%m-%dT%H:%M:%SZ'),
               'enddate': search_params[1].strftime('%Y-%m-%dT%H:%M:%SZ'),
               'region': search_params[2],
               'coordinates': search_params[3],
               'producttype': 'LANDSAT_8_C1',
               'cloud': search_params[4],
               'username': search_params[8],
               'password': search_params[9],
               'output_path': os.path.join(search_params[5], "l8_tiles")}

    #download landsat files
    l8 = landsat.download_landsat(**l8_args)
    l8_results = l8.search()

    assert len(l8_results) == 2
    assert l8_results[0]['entityId'] == 'LC82010312019151LGN00'
    assert l8_results[1]['entityId'] == 'LC82000312019160LGN00'
