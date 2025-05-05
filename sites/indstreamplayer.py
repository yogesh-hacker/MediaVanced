import requests
import re
import json
from urllib.parse import urlparse
import sys

# [TAG] IndStreamPlayer #

'''
Supports:
https://asiow333rnva.com/
https://denni348sof.com/
https://diego343qop.com/
https://dplur342dmx.com/
https://dumjo347cug.com/
https://fino338khhe.com/
https://ftmoh345xme.com/
https://hi351sinoom.com/
https://hlils336miq.com/
https://hokpi334amve.com/
https://jerry350kiz.com/
https://jillw337rpo.com/
https://jole340erun.com/
https://jolls346dae.com/
https://kinne341wokre.com/
https://route7ind.com/
https://simba344doe.com/
https://sopt339qumi.com/
https://vista335lopq.com/
https://vitea349ina.com/
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
base_url = "https://hi351sinoom.com/play/tt13622970"
parsed_url = urlparse(base_url)
default_domain = f"{parsed_url.scheme}://{parsed_url.netloc}"

headers = {
    'Referer': default_domain,
    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36'
}

# Get initial text response from base URL
response = requests.get(base_url, headers=headers).text

# Extract file URL from response
match = re.search(r'"file":"([^"]+)"', response)
if not match:
    sys.exit("File URL not found")
file_url = match.group(1).replace('\\/', '/')

# Extract the key from response
match = re.search(r'"key":"([^"]+)"', response)
if not match:
    sys.exit("Key not found")
key = match.group(1).replace('\\/', '/')

# Fetch playlist info using the extracted key
headers['X-CSRF-TOKEN'] = key
response = requests.post(file_url, headers=headers).json()

# Fetch playlist URLs with language labels
final_playlist = [
    {
        'lang': item['title'],
        'url': requests.post(f"{default_domain}/playlist/{item['file'].replace('~', '')}.txt", headers=headers).text
    }
    for item in response
]

# Print results
print("\n" + "#" * 25 + "\n" + "#" * 25)
for playlist in final_playlist:
    print(f'\n[{playlist['lang']}]: {Colors.okgreen}{playlist['url']}{Colors.endc}')
print("\n" + "#" * 25 + "\n" + "#" * 25 + "\n")
