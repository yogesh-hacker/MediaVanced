import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

'''
Supports:
https://m.ok.ru/
https://ok.ru/
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
base_url = 'http://ok.ru/video/10227378817766'
user_agent = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"
default_domain = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(base_url))
headers = {
    'Referer': default_domain,
    'User-Agent': user_agent
}

# Quality mapping
quality_map = {
    "mobile": "144p",
    "lowest": "240p",
    "low": "360p",
    "sd": "480p",
    "hd": "720p",
    "full": "1080p"
}

# Fetch page content
response = requests.get(base_url, headers=headers).text
soup = BeautifulSoup(response, 'html.parser')

# Find the video container
video_container = soup.select_one('div.one-video-player-container')

# Get JSON string from data-options
data_options = video_container.get('data-options')

# Parse JSON into dict
video_info = json.loads(data_options)

# Extract all video streams
videos = video_info['flashvars']['metadata']['videos']

# Map qualities to URLs
mapped_urls = {quality_map[item['name']]: item['url'] for item in videos}

# Extract video URL and pick max quality
max_quality = max(mapped_urls.keys(), key=lambda q: int(q.replace('p', '')))
video_url = mapped_urls[max_quality]

# Print results
print("\n" + "#" * 25 + "\n" + "#" * 25)
print(f"Captured [{Colors.okcyan}{max_quality}{Colors.endc}] URL: {Colors.okgreen}{video_url}{Colors.endc}")
print("#" * 25 + "\n" + "#" * 25)
print(f"{Colors.warning}### Use these headers to access the URL")

# Print headers by key: value
for key, value in headers.items():
    print(f"{Colors.okcyan}{key}:{Colors.endc} {value}")
print("\n")