#APIs
import pytest
import argparse

import os
import zipfile, tarfile

from sat_modules import utils_test

@pytest.fixture
def unzip_params():

    main_path = '/home/ubuntu/Dani/git/sat/data'

    s2_path = os.path.join(main_path, 's2_tiles')
    s2_bands = []

    l8_path = os.path.join(main_path, 'l8_tiles')
    l8_bands = ['BAND_1', 'BAND_2', 'BAND_3', 'BAND_4', 'BAND_5', 'BAND_6', 'BAND_7', 'BAND_8', 'BAND_9', 'BAND_10', 'BAND_11']

    return [s2_path, l8_path, s2_bands, l8_bands]


def test_unzip_esa(unzip_params):

    path = unzip_params[0]
    s2_tiles = os.listdir(path)

    for tile in s2_tiles:

        name = tile.split('.')[0]
        tile_path = os.path.join(path, tile)

        with zipfile.ZipFile(tile_path, 'r') as zip_ref:
            zip_ref.extractall(path)

        folder = os.path.join(path, '{}.SAFE'.format(name))
        raster = utils_test.esa_config_file(folder)
        datasets = raster.GetSubDatasets()

        assert len(datasets) == 4

def test_unzip_nasa(unzip_params):

    path = unzip_params[1]
    l8_tiles = os.listdir(path)
    l8_bands = unzip_params[3]

    for tile in l8_tiles:

        name = tile.split('.')[0]
        tile_path = os.path.join(path, tile)

        with zipfile.ZipFile(tile_path, 'r') as zip_ref:
            zip_ref.extractall(path)

        folder = os.path.join(path, name)
        config = utils_test.nasa_config_file(folder)
        config = config['L1_METADATA_FILE']

        for band in l8_bands:

            band_name = config['PRODUCT_METADATA']['FILE_NAME_{}'.format(band)]
            band_name = band_name.replace('"',"")
            band_path = os.path.join(folder, band_name)
            assert os.path.isfile(band_path) == True
