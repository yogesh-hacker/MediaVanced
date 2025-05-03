import requests
from bs4 import BeautifulSoup
import re

'''
Supports:
https://filelions.site/
'''

class Colors:
    header = '\033[95m'
    okblue = '\033[94m'
    okcyan = '\033[96m'
    okgreen = '\033[92m'
    warning = '\033[93m'
    fail = '\033[91m'
    endc = '\033[0m'
    bold = '\033[1m'
    underline = '\033[4m'

# Constants
default_domain = "https://filelions.site/"
base_url = "https://niikaplayerr.com/f/gxzkamnuf9x3"
headers = {
    'Referer': default_domain
}

# Fetch response
response = requests.get(base_url, headers=headers).text

print(response)

#mRegex = r'file:"([^"]+)"'
