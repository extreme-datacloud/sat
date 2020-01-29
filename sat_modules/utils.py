# -*- coding: utf-8 -*-

# Copyright 2018 Spanish National Research Council (CSIC)
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""
Satellite utils

Author: Daniel Garcia Diaz
Date: May 2018
"""

#Submodules
from sat_modules import config

#APIs
import zipfile, tarfile
import argparse

import os
import io

import datetime
from six import string_types


def valid_date(sd, ed):
    """
    check if the format date input is string("%Y-%m-%d") or datetime.date
    and return it as format strftime("%Y-%m-%dT%H:%M:%SZ")

    Parameters
    ----------
    sd(start_date) : str "%Y-%m-%d"
    ed(end_date) : str "%Y-%m-%d"

    Returns
    -------
    sd : datetime
        strftime("%Y-%m-%dT%H:%M:%SZ")
    ed : datetime
        strftime("%Y-%m-%dT%H:%M:%SZ")

    Raises
    ------
    FormatError
        Unsupported format date
    ValueError
        Unsupported date value
    """

    if isinstance(sd, datetime.date) and isinstance(ed, datetime.date):

        return sd.strftime("%Y-%m-%dT%H:%M:%SZ"), ed.strftime('%Y-%m-%dT%H:%M:%SZ')

    elif isinstance(sd, string_types) and isinstance(ed, string_types):    
        try:
            sd = datetime.datetime.strptime(sd, "%Y-%m-%d")
            ed = datetime.datetime.strptime(ed, "%Y-%m-%d")
            if sd < ed:
                return sd.strftime("%Y-%m-%dT%H:%M:%SZ"), ed.strftime("%Y-%m-%dT%H:%M:%SZ")
            else:
                msg = "Unsupported date value: '{} or {}'.".format(sd, ed)
                raise argparse.ArgumentTypeError(msg)
        except:
            msg = "Unsupported format date: '{} or {}'.".format(sd, ed)
            raise argparse.ArgumentTypeError(msg)
    else:
        msg = "Unsupported format date: '{} or {}'.".format(sd, ed)
        raise argparse.ArgumentTypeError(msg)


def valid_region(region, coord = None):
    """
    check if the region exits in the config file

    Parameters
    ----------
    coordinates: list of coordinates

    Raises
    ------
    FormatError
            Not a valid region
    """

    if region in config.regions:

        coordinates = config.regions[region]

    else:

        #Hacer saltar el widget del mapa

        W = round(-360.0 + float(coord.split('[')[2][:8]), 4)
        S = float(coord.split('[')[2][-11:-4])
        E = round(-360.0 + float(coord.split('[')[4][:8]), 4)
        N = float(coord.split('[')[4][-11:-4])

        coordinates = {}
        coordinates['W'], coordinates['S'] = W, S
        coordinates['E'], coordinates['N'] = E, N

    return coordinates


def open_compressed(byte_stream, file_format, output_folder):
    """
    Extract and save a stream of bytes of a compressed file from memory.
    Parameters
    ----------
    byte_stream : bytes
    file_format : str
        Compatible file formats: tarballs, zip files
    output_folder : str
        Folder to extract the stream
    Returns
    -------
    Folder name of the extracted files.
    """

    tar_extensions = ['tar', 'bz2', 'tb2', 'tbz', 'tbz2', 'gz', 'tgz', 'lz', 'lzma', 'tlz', 'xz', 'txz', 'Z', 'tZ']
    if file_format in tar_extensions:
        tar = tarfile.open(mode="r:{}".format(file_format), fileobj=io.BytesIO(byte_stream))
        tar.extractall(output_folder)
        folder_name = tar.getnames()[0]
        return os.path.join(output_folder, folder_name)

    elif file_format == 'zip':
        zf = zipfile.ZipFile(io.BytesIO(byte_stream))
        zf.extractall(output_folder)
        folder_name = zf.namelist()[0].split('/')[0]
        return os.path.join(output_folder, folder_name)

    else:
        raise ValueError('Invalid file format for the compressed byte_stream')

