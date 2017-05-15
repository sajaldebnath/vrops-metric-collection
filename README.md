# vrops-metric-collection
Collect any resource metric from vRealize Operations Manager using REST API and python client

Purpose: 
This is a small program to collect metric data of a "resource/set of resources" from vRealize Operations Manager using python client and REST API. This can collect a single value of the metric or a series of historical values.

What is included:

There are two program files, set-config.py and metric-collection.py. The above two programs generate two data files config.json and metric-data.json. Sample is provided for config.json and metric-data.json

Pre-Requisites:

These programs were written in Python2.7 version.So your system should have Python 2.7.
Also download and install nagini module from vRealize Operations Manager. It can be found at "https:///suite-api" . Visit the page, download and install the Python Client.

How to run:

Download both "set-config.py" and "metric-collection.py" to the same location. Program has two parts.

Part 1: Setting up the environment: 

First time run set-config.py with #python set-config.py, this will ask for the following inputs:

Adapter Kind: 
Resource Kind: 
vROPs server IP/FQDN: 
user id: 
vROps password: 
Maximum number of samples to collect:
Number of Keys to Monitor: Keys (one by one):

Once all the above information is provided, the script generates config.json in the same location. The provided password is saved in encrypted format.

Part 2: Getting the actual data:

Run the "metric-collection.py" file with # python metric-collection.py This will get values from config.json file and generate metric-data.json file in the same location. This metric-data.json will have the desired output values.

You should schedule a cron job or scheduler to run this script every 6 minutes (considering vROps collects data every 5 minutes). This way every 6 minutes you will get fresh data and parse the data as per your requirement.

Check the format of the metric-data.json file to further utilize the data.

Points to Note: 

By default, I am not collecting historical data (MaxSample is default 1), so I get the last data. This should be run as a cron job to get continuous data. To get the historical data add the MaxSample value as any non-zero integer value
