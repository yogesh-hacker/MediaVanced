import re
import requests
from urllib.parse import urlparse

'''
Supports:
https://hlscdn.xyz/
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
base_url = "https://hlscdn.xyz/e/299686-03"
user_agent = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36"
default_domain = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(base_url))
headers = {
    "Referer": default_domain,
    "User-Agent": user_agent,
    "X-Requested-With": "XMLHttpRequest",
}

# Fetch page content
response = requests.get(base_url, headers=headers).text

# Get token and stream info
token = re.search(r'window\.kaken=\"(.*?)\"', response).group(1)
response = requests.get(f'https://hlscdn.xyz/api', data=token, headers=headers).json()

# Extract video URL
video_url = response.get('sources')[0].get('file')

print("\n" + "#" * 25 + "\n" + "#" * 25)
print(f"Captured URL: {Colors.okgreen}{video_url}{Colors.endc}")
print("#" * 25 + "\n" + "#" * 25)
print(f"{Colors.warning}### Use these headers to access the URL")
print(f"{Colors.okcyan}Referer:{Colors.endc} {default_domain}")
print("\n")