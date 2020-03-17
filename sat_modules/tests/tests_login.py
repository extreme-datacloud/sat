#imports APIs
import argparse
import requests

def ESA_login(url, credentials):

    session = requests.Session()

    #API connexion
    session.auth = (credentials["username"], credentials["password"])
    response = session.get(url, auth=session.auth)

    return response.status_code


def NASA_login(url, credentials):

    session = requests.Session()

    #API connexion
    session.auth = (credentials["username"], credentials["password"])
    response = session.get(url, auth=session.auth)

    return response.status_code

def test_login():

    #url api
    ESA_url = 'https://scihub.copernicus.eu/apihub/'
    #Sentinel credentials
    ESA_credentials = {'username':"lifewatch", 'password':"xdc_lfw_data"}

    #correct status code
    ok_status = 200

    assert ESA_login(ESA_url, ESA_credentials) == ok_status

    # API
    NASA_url = 'https://ers.cr.usgs.gov/login/'
    #credentials
    NASA_credentials = {'username':"lifewatch", 'password':"xdc_lfw_data2018"}

    assert NASA_login(NASA_url, NASA_credentials) == ok_status
