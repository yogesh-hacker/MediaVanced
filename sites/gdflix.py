import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs

'''
Supports:
https://*.gdflix.net/
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
base_url = 'https://new9.gdflix.net/file/Az2BwXqiFfjERq0'
user_agent = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"
default_domain = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(base_url))
headers = {
    'Referer': default_domain,
    'User-Agent': user_agent
}

# Fetch page content
response = requests.get(base_url, headers=headers).text
soup = BeautifulSoup(response, 'html.parser')


# Find all valid downloading URLs
anchor_tags = soup.find_all('a')
valid_urls = []
for anchor in anchor_tags:
    style = anchor.get('style')
    href  = anchor.get('href')
    if not style or 'min-width' not in style:
        continue
    if href and href.startswith('http'):
        valid_urls.append(href)

# Use Instant DL URL(Best)
instant_dl = next((url for url in valid_urls if 'instant' in url), None)

# Fetch download page
response = requests.get(instant_dl, headers=headers, allow_redirects = False)
redirect_url = response.headers.get('Location')

# Extract video URL
video_url = redirect_url.split('?url=')[-1]

# Print results
print("\n" + "#" * 25 + "\n" + "#" * 25)
print(f"Captured URL: {Colors.okgreen}{video_url}{Colors.endc}")
print("#" * 25 + "\n" + "#" * 25)
print("\n")