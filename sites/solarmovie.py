import re
import time
import random
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

'''
Supports:
https://ww2.solarmovie.id/
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
base_url = 'https://ww2.solarmovie.id/movie/kgf-chapter-2-sub-eng/DcmB7TGV/iHmWmYKs'
user_agent = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"
default_domain = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(base_url))
headers = {
    'Referer': default_domain,
    'User-Agent': user_agent
}

# Fetch page content
response = requests.get(base_url, headers=headers).text
soup = BeautifulSoup(response, 'html.parser')

# Get video page URL
regex = r"history.pushState\(\{\},\'\',\s*\'\/(.*?)\'"
match = re.search(regex, response)
if not match:
    canonical = soup.find('link', attrs={'rel': 'canonical'}).get('href')
    response = requests.get(canonical, headers=headers).text
    match = re.search(regex, response)
video_page_url = f"{default_domain}{match.group(1)}" if match else None

# Get streaming sources
api_url = f'{video_page_url}?number=1&r={random.random()}&_={int(time.time() * 1000)}'
response = requests.get(api_url, headers={**headers, 'X-Requested-With': 'XMLHttpRequest'}).json()

# Extract video URL
max_quality = max(response, key=lambda x: x['label'])
video_url = max_quality.get('src')

# Print results
print("\n" + "#" * 25 + "\n" + "#" * 25)
print(f"Captured URL: {Colors.okgreen}{video_url}{Colors.endc}")
print("#" * 25 + "\n" + "#" * 25)
print("\n")