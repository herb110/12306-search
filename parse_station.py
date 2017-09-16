import re 
import requests
from pprint import pprint
import ssl
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import json
import os
import codecs
#import urllib.request import urlopen

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
#ssl._create_default_https_context = ssl._create_unverified_context
url = 'https://kyfw.12306.cn/otn/resources/js/frameworkl/station_name.js?station_version=1.9025'
response = requests.get(url, verify = False)
with open('station_name.js','rb') as f:
    response = f.read().decode('utf-8')
    f.close()
stations = re.findall(u'([\u4e00-\u9fa5]+)\|([A-Z]+)',response)
pprint(dict(stations),indent = 4)