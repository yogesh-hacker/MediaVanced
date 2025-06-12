import requests
import re
import os
from bs4 import BeautifulSoup
import os
from pathlib import Path
import base64
import binascii
import codecs
import time
from urllib.parse import urlparse

'''
Supports:
https://clickndownload.cfd/
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
base_url = "https://clickndownload.cfd/mnoso4chus5s"
user_agent = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36"
default_domain = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(base_url))
headers = {
    'Referer': default_domain,
    'Accept': '*/*',
    'User-Agent': user_agent
}

# Fetch page content
response = requests.get(base_url, headers=headers).text
soup = BeautifulSoup(response, 'html.parser')

# Get form input values
form = soup.select_one('form')
inputs = form.find_all('input')
data = {}
for input in inputs:
    data[input['name']] = input['value']

# Post data contents
response = requests.post(base_url, headers=headers, data=data).text
soup = BeautifulSoup(response, 'html.parser')

# Get form input values
form = soup.select_one('form')
inputs = form.find_all('input')
data = {}
for input in inputs:
    data[input['name']] = input.get('value', '0')

# Post data contents
print('Wait 15 seconds...!')
time.sleep(15)
response = requests.post(base_url, headers=headers, data=data).text
soup = BeautifulSoup(response, 'html.parser')

# Get Video URL
anchor_tag = soup.select_one('a.downloadbtn')
video_url = anchor_tag['href']

# Print results
print("\n" + "#" * 25 + "\n" + "#" * 25)
print(f"Captured URL: {Colors.okgreen}{video_url}{Colors.endc}")
print("#" * 25 + "\n" + "#" * 25)
print("\n")