#import APIs
import datetime

from sat_modules import sentinel
from sat_modules import landsat

def test_search():

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
    s2_results = s2.search()

    assert len(s2_results) == 2
    assert s2_results[0]['title'] == 'S2A_MSIL1C_20190608T105621_N0207_R094_T30TWM_20190608T130706'
    assert s2_results[1]['title'] == 'S2B_MSIL1C_20190603T105629_N0207_R094_T30TWM_20190603T131528'


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
    l8_results = l8.search()

    assert len(l8_results) == 2
    assert l8_results[0]['entityId'] == 'LC82010312019151LGN00'
    assert l8_results[1]['entityId'] == 'LC82000312019160LGN00'
