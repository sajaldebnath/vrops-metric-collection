# !/usr/bin python

"""
#
# set-config - a small python program to setup the configuration environment for data-collect.py
# data-collect.py contain the python program to gather Metrics from vROps
# Author Sajal Debnath <sdebnath@vmware.com> 
#
"""
# Importing the required modules

import json
import base64
import os,sys


# Getting the absolute path from where the script is being run
def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))

def get_the_inputs():
    adapterkind = raw_input("Please enter Adapter Kind: ")
    resourceKind = raw_input("Please enter Resource Kind: ")
    servername = raw_input("Enter enter Server IP/FQDN: ")
    serveruid = raw_input("Please enter user id: ")
    serverpasswd = raw_input("Please enter vRops password: ")
    encryptedvar = base64.b64encode(serverpasswd)
    maxsamples = raw_input("Please enter the maximum number of samples to collect: ")

    keys_to_monitor = raw_input("Please enter the number of keys to monitor: ")

    keys = []
    for i in range(int(keys_to_monitor)):
        keys.append(raw_input("Enter the key: "))
    data = {}

    if int(maxsamples) < 1:
        maxsamples = 1


    data["adapterKind"] = adapterkind
    data["resourceKind"] = resourceKind
    data["sampleno"] = int(maxsamples)
    serverdetails = {}
    serverdetails["name"] = servername
    serverdetails["userid"] = serveruid
    serverdetails["password"] = encryptedvar

    data["server"] = serverdetails
    data["keys"] = keys

    return data


# Getting the path where config.json file should be kept
path = get_script_path()
fullpath = path+"/"+"config.json"

# Getting the data for the config.json file
final_data = get_the_inputs()

# Saving the data to config.json file

with open(fullpath, 'w') as outfile:
    json.dump(final_data, outfile, sort_keys = True, indent = 2, separators=(',', ':'), ensure_ascii=False)