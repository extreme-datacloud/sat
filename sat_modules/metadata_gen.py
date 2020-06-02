import xml.etree.cElementTree as ET
import xmltodict
import os
import json
import requests
import datetime
import numpy as np
from netCDF4 import Dataset

from sat_modules import config

def metadata_gen(title,dateIni,dateEnd,geographicDesc,westBounding,eastBounding,northBounding,southBounding,params):

    #EML-XML Header
    ET.register_namespace('eml',"eml://ecoinformatics.org/eml-2.1.1") #some name
    eml = ET.Element("{eml://ecoinformatics.org/eml-2.1.1}eml",system="knb" )
    #eml = ET.Element("eml:eml",system="knb",xmlns="eml://ecoinformatics.org/eml-2.1.1")

    #-Access
    acceso = ET.SubElement(eml, "access", authSystem="knb", order="allowFirst")
    permiso=ET.SubElement(acceso,"allow")
    ET.SubElement(permiso,"principal").text="public"
    ET.SubElement(permiso,"permission").text="read"

    #-Dataset Module
    dataset=ET.SubElement(eml,"dataset")
    ET.SubElement(dataset,"title").text=title

    #--Coverage
    coverage=ET.SubElement(dataset,"coverage")

    #---Geographic Coverage
    coverageG=ET.SubElement(coverage,"geographicCoverage",id='id')
    ET.SubElement(coverageG,"geographicDescription").text=geographicDesc
    ET.SubElement(coverageG,"westBoundingCoordinate").text=westBounding
    ET.SubElement(coverageG,"eastBoundingCoordinate").text=eastBounding
    ET.SubElement(coverageG,"northBoundingCoordinate").text=northBounding
    ET.SubElement(coverageG,"southBoundingCoordinate").text=southBounding

    #---Temporal Coverage
    coverageT=ET.SubElement(coverage,"temporalCoverage")
    #---SingleData
    #----TODO
    #---rangeOfDates
    rangeOfDates=ET.SubElement(coverageT,"rangeOfDates")
    #----beginDate
    ET.SubElement(ET.SubElement(rangeOfDates,"beginDate"),"calendarDate").text=dateIni
    #---endDate
    ET.SubElement(ET.SubElement(rangeOfDates,"endDate"),"calendarDate").text=dateEnd

    tree = ET.ElementTree(eml)

    #Escribimos los datos en un archivo or onedata attachement

    xml_path = os.path.join(config.datasets_path, geographicDesc, '{}.xml'.format(title))
    tree.write(xml_path, encoding='UTF-8', xml_declaration=True)

    if (config.onedata_mode == 1):
        try:
            token = os.environ['ONECLIENT_AUTHORIZATION_TOKEN']
        except KeyError:
            token = 'MDAyOGxvY2F00aW9uIG9uZXpvbmUuY2xvdWQuY25hZi5pbmZuLml00CjAwMzBpZGVudGlmaWVyIDgzNTUyMjE1NGE3MDJlMDAzMDBhYTMyZjVlYmJlMmEyCjAwMWFjaWQgdGltZSA8IDE2MTczOTA3NDIKMDAyZnNpZ25hdHVyZSDvvdYf8B00MXmo8N9rokRgjCKyijYR35dOZi602ibmfZVgo'
        header_json = {'X-Auth-Token': token, 'Content-type' : 'application/json'}
        try:
            print('onedata_url:  {}'.format(config.onedata_url))
            print('onedata_api:  {}'.format(config.onedata_api))
            print('onedata_space: {}'.format(config.onedata_space))
            print ('Region:  {}'.format(geographicDesc))
            print ('tile:  {}'.format(title))

            url = '{}{}metadata/json/{}/{}/{}'.format(config.onedata_url, config.onedata_api, config.onedata_space, geographicDesc, title)
            r = requests.put(url, headers=header_json, data=eml_to_json(xml_path))
            print("Metadata attachement: %i" % r.status_code)
            os.remove(xml_path)

        except requests.exceptions.RequestException as e:

            print('onedata_url:  {}'.format(config.onedata_url))
            print('onedata_api:  {}'.format(config.onedata_api))
            print('onedata_space: {}'.format(config.onedata_space))
            print ('Region:  {}'.format(geographicDesc))
            print ('tile:  {}'.format(title))

            print(e)

def file_block_csv(title,params,parent):
    dataTable=ET.SubElement(parent,"dataTable", id=title)
    ET.SubElement(dataTable,"entityName").text=title
    phisical = ET.SubElement(dataTable,"physical")
    ET.SubElement(phisical,"objectName").text=title
    ET.SubElement(phisical,"size", unit="bytes").text="1231" #TODO
    ET.SubElement(phisical,"characterEncoding").text="ASCII"

    dataFormat = ET.SubElement(phisical,"dataFormat")
    textFormat = ET.SubElement(dataFormat,"textFormat")

    ET.SubElement(textFormat,"numHeaderLines").text="1" #TODO
    ET.SubElement(textFormat,"attributeOrientation").text="column"
    ET.SubElement(ET.SubElement(textFormat,"simpleDelimited"),"fieldDelimiter").text="\\t"

    #--Attribute list
    dataTable = attribute_block_csv(params,dataTable)
    return parent


def attribute_block_csv(params,dataTable):
    print("PARAMS")
    print(params)
    #TODO Complete
    attributeList=ET.SubElement(dataTable,"attributeList")
    for att in params:
        if att == "Date":
            attribute=ET.SubElement(attributeList,"attribute",id="Date")
            ET.SubElement(attribute,"attributeName").text="Date"
            ET.SubElement(attribute,"attributeDefinition").text="Date"
            ET.SubElement(attribute,"formatString").text="YYYY-MM-DD"

        elif att == "Temp":
            attribute=ET.SubElement(attributeList,"attribute",id="Temp")
            ET.SubElement(attribute,"attributeName").text="Temperature"
            ET.SubElement(attribute,"attributeLabel").text="Temp"
            ET.SubElement(attribute,"attributeDefinition").text="Temperature" 
            ET.SubElement(attribute,"standardUnit").text="Celsius"

        elif att == "Wind_Speed":
            attribute=ET.SubElement(attributeList,"attribute",id="Wind_Speed")
            ET.SubElement(attribute,"attributeName").text="Wind_Speed"
            ET.SubElement(attribute,"attributeLabel").text="Wind_Speed"
            ET.SubElement(attribute,"attributeDefinition").text="Average wind speed"
            ET.SubElement(attribute,"standardUnit").text="m/s"

        elif att == "Wind_Dir":
            attribute=ET.SubElement(attributeList,"attribute",id="Wind_Dir")
            ET.SubElement(attribute,"attributeName").text="Wind_Dir"
            ET.SubElement(attribute,"attributeLabel").text="Wind_Dir"
            ET.SubElement(attribute,"attributeDefinition").text="Wind direction"
            ET.SubElement(attribute,"standardUnit").text="degrees"

        elif att == "ID":
            attribute=ET.SubElement(attributeList,"attribute",id="ID")
            ET.SubElement(attribute,"attributeName").text="ID"
            ET.SubElement(attribute,"attributeLabel").text="ID"
            ET.SubElement(attribute,"storageType").text="string"

    return dataTable


def eml_to_json(xml_file):
    with open(xml_file, "rb") as f:
        o = xmltodict.parse(f, xml_attribs=True)
    result = json.dumps(o)
    return result


def list_onedata_views(onedata_token):
    headers = {"X-Auth-Token": onedata_token}
    space_id = "ecf6abbd4fcd6d6c9b505d5f5e82f94c"
    url = ("https://vm027.pub.cloud.ifca.es"
       "/api/v3/oneprovider/spaces/%s/views/" %
           space_id)
    r = requests.get(url, headers=headers)
    return json.loads(r.content)["views"]


def create_filename_view(onedata_token):
    headers = {"X-Auth-Token": onedata_token}
    url = ("https://vm027.pub.cloud.ifca.es"
           "/api/v3/oneprovider/spaces/ecf6abbd4fcd6d6c9b505d5f5e82f94c")
    r = requests.get(url, headers=headers)
#    space_id = json.loads(r.content)['spaceId']
    space_id= 'ecf6abbd4fcd6d6c9b505d5f5e82f94c'
    data = open('/wq_sat/views/view_filename.js','rb')
    print ('data_ {}'.format(data))
    print('Searching models')
    index_name = 'filename'
    url = ("https://vm027.pub.cloud.ifca.es"
           "/api/v3/oneprovider/spaces/%s/views/%s?spatial=false" % (
               space_id, index_name))
    r = requests.put(url, data = data, headers = headers)
    return r.status_code


def create_landsat_date_view(onedata_token):
    headers = {"X-Auth-Token": onedata_token}
    url = ("https://vm027.pub.cloud.ifca.es"
           "/api/v3/oneprovider/spaces/ecf6abbd4fcd6d6c9b505d5f5e82f94c")
    r = requests.get(url, headers=headers)
    print ("url 1: {}".format(url))
    space_id = 'ecf6abbd4fcd6d6c9b505d5f5e82f94c'
    data = open('/wq_sat/views/view_dates_landsat.js','rb')
    index_name = 'view_date_landsat'
    url = ("https://vm027.pub.cloud.ifca.es"
           "/api/v3/oneprovider/spaces/%s/views/%s?spatial=false" % (
               space_id, index_name))
    print ("url 2: {}".format(url))
    r = requests.put(url, data = data, headers = headers)
    print ("create r: {}".format(r))
    return r.status_code


def is_downloaded(onedata_token, filename):
    headers = {"X-Auth-Token": onedata_token}
    url = ("https://vm027.pub.cloud.ifca.es"
           "/api/v3/oneprovider/spaces/ecf6abbd4fcd6d6c9b505d5f5e82f94c")
    r = requests.get(url, headers=headers)
#    space_id = json.loads(r.content)['spaceId']
    space_id= 'ecf6abbd4fcd6d6c9b505d5f5e82f94c'
    index_name = 'filename'

    if index_name not in list_onedata_views(onedata_token):
        create_filename_view(onedata_token)
    url = ("https://vm027.pub.cloud.ifca.es"
           "/api/v3/oneprovider/spaces/%s/views/%s/query?spatial=false&stall=false" % (
               space_id, index_name))
    r = requests.get(url, headers=headers)
    response = json.loads(r.content)

    result = False

    if len(response) == 0:
        return result
    elif len(response) == 1:
        response = response[0]['key']
    elif len(response) == 2:
        response = response[0]['key'] + response[1]['key']

    if filename in response:
        result = True

    return result

#date is a string yyyy-mm-dd
def find_closest_date(onedata_token, date, region):

    headers = {"X-Auth-Token": onedata_token}

    date_time_obj = datetime.datetime.strptime(date, '%Y-%m-%d')
    seconds_since_epoch = date_time_obj.timestamp()
    seconds_since_epoch = int(seconds_since_epoch)*1000

    space_id = 'ecf6abbd4fcd6d6c9b505d5f5e82f94c'

    index_name = 'view_date_landsat'
    if index_name not in list_onedata_views(onedata_token):
        create_landsat_date_view(onedata_token)

    url = ("https://vm027.pub.cloud.ifca.es"
           "/api/v3/oneprovider/spaces/%s/views/%s/query?spatial=false&stall=false" % (
               space_id, index_name))
    r = requests.get(url, headers=headers)
    value = ''
    min = 999999999999999
    for e in json.loads(r.content):
        if e['value'][0] == region:
            if min > abs(seconds_since_epoch - e['key']):
                min = abs(seconds_since_epoch - e['key'])
                value = e['value'][1]

    return value

def model_temp(onedata_token, date, region):

    l8_file = find_closest_date(onedata_token, date, region)
    file_path = os.path.join(config.datasets_path, region, l8_file)
    dataset= Dataset(file_path, 'r', format='NETCDF4_CLASSIC')
    variables = dataset.variables

    G = dataset.variables['SRB3'][:]
    NIR = dataset.variables['SRB5'][:]

    mndwi = (G - NIR) / (G + NIR)
    mndwi[mndwi <=0] = np.nan
    mndwi = np.ma.masked_where(condition=np.isnan(mndwi), a=mndwi)

    B11 = dataset.variables['SRB11'][:]
    B11[mndwi.mask] = np.nan
    B11 = np.ma.masked_where(condition=np.isnan(B11), a=B11)
    Temp = np.mean(B11) - 273.15

    return Temp

