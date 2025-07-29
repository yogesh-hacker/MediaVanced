import re
import requests
import pyjson5 as json
from bs4 import BeautifulSoup
from urllib.parse import urlencode, urlparse, parse_qs, urlunparse

'''
Supports:
https://streamingcommunityz.info/
https://vixcloud.co/
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
base_url = 'https://streamingcommunityz.info/it/watch/12704'
user_agent = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36"
default_domain = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(base_url))
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Referer': default_domain,
    'User-Agent': user_agent
}

# Sanitize base URL
if 'watch' in base_url:
    base_url = base_url.replace('watch', 'iframe')

# Fetch page content
response = requests.get(base_url, headers=headers).text
soup = BeautifulSoup(response, 'html.parser')

# Get inner iframe(vixcloud)
iframe_url = soup.select_one("iframe")['src']
headers['Referer'] = iframe_url

# Get video page
response = requests.get(iframe_url, headers=headers).text
playlist_data = re.search(r'window\.masterPlaylist\s*=\s*(\{[\s\S]*?\})\n', response)
playlist_info = json.loads(playlist_data.group(1))

# Extract base URL and parameters
master_url = playlist_info['url']
params = playlist_info['params']

# Merge with existing query params in the URL
parsed_url = urlparse(master_url)
existing_params = parse_qs(parsed_url.query)

# Update with new params
merged_params = {**existing_params, **params}

# Make params list and add valid params
merged_params = {k: v if isinstance(v, list) else [v] for k, v in merged_params.items()}
merged_params['h'] = '1'

# Flatten all values for urlencode
flattened = {k: v[0] for k, v in merged_params.items() if v[0] != ''}

# Extract video URL
new_queries = urlencode(flattened)
video_url = urlunparse(parsed_url._replace(query=new_queries))

# Print results
print("\n" + "#" * 25 + "\n" + "#" * 25)
print(f"Captured URL: {Colors.okgreen}{video_url}{Colors.endc}")
print("#" * 25 + "\n" + "#" * 25)
print("\n")
