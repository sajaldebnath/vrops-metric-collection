# !/usr/bin python

"""
#
# data-collect.py contain the python program to gather Metrics from vROps. Before you run this script
# set-config.py should be run once to set the environment
# Author Sajal Debnath <sdebnath@vmware.com> 
#
"""
# Importing the Modules

import nagini
import requests
#import pprint
import json
import os, sys
import base64
import time
from requests.packages.urllib3.exceptions import InsecureRequestWarning



# Function to get the absolute path from where the script is being run
def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))

# Function to get the metric data
def get_metric_data(resourceknd,adapter,key,sampleno ):
    outdata = [] # It's going to store the final JSON data
    # Gettting a list of resources which matches the criteria or resourceKind and adapterKind
    for resource in vrops.get_resources(resourceKind=resourceknd, adapterKindKey=adapter)['resourceList']:

        allstat = {} # This variable will hold all the statistics of all resources
        resourcedata = {} # This variable is going to hold value for individual resource

        # print (resource['identifier'], resource['resourceKey']['name'])
        name = resource['identifier']

        # Gettting the metric values for the keys of a particular resource
        allvalues = vrops.get_latest_stats(resourceId=name, statKey=key,maxSamples=sampleno, id=name)

        # Building the components of the output JSON file
        resourcedata["identifier"] = resource['identifier']
        resourcedata["name"] = resource['resourceKey']['name']

        # Checking for any null values
        if not allvalues["values"]:
            continue
        else:
            if int(sampleno) == 1:
                for value in allvalues["values"][0]["stat-list"]["stat"]:
                    allstat[value["statKey"]["key"]] = value["data"][0]

            else:

                # We have a range of values to store
                for singlevalue in allvalues["values"][0]["stat-list"]["stat"]:
                    # pp.pprint(value)
                    all_metric_data = []
                    sample = len(singlevalue["data"])
                    for i in range(sample):
                        metric_data = {}
                        metric_data["value"] = singlevalue["data"][i]
                        metric_data["timestamp"] = singlevalue["timestamps"][i]

                        all_metric_data.append(metric_data)

                    allstat[singlevalue["statKey"]["key"]] = all_metric_data


        resourcedata["stats"] = allstat

        outdata.append(resourcedata)

    return outdata



# Disabling the warning sign for self signed certificates. Remove the below line for CA certificates
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
#pp = pprint.PrettyPrinter(indent=2)


# Getting the absolute path from where the script is being run
path = get_script_path()
fullpath = path+"/"+"config.json"

# Opening the config.json file to read the parameters from
with open(fullpath) as data_file:
    data=json.load(data_file)



# Reading the parameters from config.json file
key = []
adapter = data["adapterKind"]
resourceknd = data["resourceKind"]
servername = data["server"]["name"]
passwd = base64.b64decode(data["server"]["password"])
uid = data["server"]["userid"]
sampleno = data["sampleno"]
# Getting the list of Keys for which to collect metrics
for i in data["keys"]:
    key.append(i)


# connecting to the vROps server
#print("Connecting to vROps")
vrops = nagini.Nagini(host=servername, user_pass=(uid, passwd))

"""
Getting Token

vrops = nagini.Nagini(host=servername, user_pass=(uid, passwd) )

serverdata={}
serverdata["username"] = uid
serverdata["password"] = passwd
serverdata["authSource"] = "Local Users"
databack = vrops.acquire_token(serverdata)

token = databack["token"]
validity = databack["validity"]

# Making further calls



"""

# Creating the output variables
outstat = {}
alldata = []


# Getting the metric data for all the resources which match the criteria
alldata = get_metric_data(resourceknd,adapter,key,sampleno )

# Creating final parameters for output JSON file
outstat["allstats"] = alldata
# print ("Completed")

outstat["timestamp"] = time.ctime()

# Getting the path to the output json file
outpath = path+"/"+"metric-data.json"

# Writing the data to output JSON file
with open(outpath, 'w') as outfile:
    json.dump(outstat, outfile, sort_keys = True, indent = 2, separators=(',', ':'), ensure_ascii=False)
