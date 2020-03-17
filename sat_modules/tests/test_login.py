#imports apis
import argparse
import requests

def ESA_login():

    #url api
    api_url = 'https://scihub.copernicus.eu/apihub/'

    #Sentinel credentials
    credentials = {'username':"lifewatch", 'password':"xdc_lfw_data"}

    #correct status code
    ok_status = 200

    session = requests.Session()

    #API connexion
    session.auth = (credentials["username"], credentials["password"])
    response = session.get(api_url, auth=session.auth)

    assert response.status_code == ok_status
