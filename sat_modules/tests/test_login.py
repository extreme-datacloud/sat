import pytest
import argparse
import requests
import sat_modules

@pytest.fixture
def login_params():
    #url api
    ESA_url = 'https://scihub.copernicus.eu/apihub/'
    #Sentinel credentials
    ESA_username = "lifewatch"
    ESA_password = "xdc_lfw_data"

    #correct status code
    ok_status = 200

    # API
    NASA_url = 'https://ers.cr.usgs.gov/login/'
    #credentials
    NASA_username = "lifewatch"
    NASA_password = "xdc_lfw_data2018"
    return [ok_status, ESA_url, ESA_username, ESA_password,
            NASA_url, NASA_username, NASA_password]


def test_esa_login(login_params):
    session = requests.Session()
    #API connexion
    session.auth = (login_params[2], login_params[3])
    response = session.get(login_params[1], auth=session.auth)

    assert response.status_code == login_params[0]

def test_nasa_login(login_params):

    session = requests.Session()

    #API connexion
    session.auth = (login_params[5], login_params[6])
    response = session.get(login_params[4], auth=session.auth)

    assert response.status_code == login_params[0]
