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

Author: Daniel García Díaz
Institute of Physics of Cantabria (IFCA)
Advanced Computing and e-Science
Date: May 2018
"""

#APIs
import os, shutil
import io

import zipfile, tarfile
import argparse

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


def get_zipfile(tile_path, gz_path):

    tar_path = '{}.tgz'.format(tile_path)

    with tarfile.open(gz_path, 'r') as tar:
        tar.extractall(tile_path)
    os.remove(gz_path)

    with tarfile.open(tar_path, "w:gz" ) as tar:
        tar.add(tile_path)
    shutil.rmtree(tile_path)
