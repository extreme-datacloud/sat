#imports apis
import os

#configure local path
local_path = "local_path"

#Sentinel credentials
sentinel_pass = {'username': "lifewatch", 'password': "xdc_lfw_data"}

#Landsat credentials
landsat_pass = {'username': "lifewatch", 'password': "xdc_lfw_data2018"}

#available regions
regions = {'CdP': {'W':-2.830, 'S':41.820, 'E':-2.690, 'N':41.910}, 'Cogotas': {'W':-4.728, 'S':40.657, 'E':-4.672, 'N':40.731}, 
'Sanabria': {'W':-6.739, 'S':42.107, 'E':-6.689, 'N':42.136}}
