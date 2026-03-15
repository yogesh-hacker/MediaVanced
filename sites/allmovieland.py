import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse



'''
Supports:
https://allmovieland.you/
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
base_url = "https://allmovieland.you/9794-ramyaa.html"
user_agent = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36"
default_domain = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(base_url))
headers = {
    'Referer': default_domain,
    'User-Agent': user_agent
}

# Request the main page which contains embed configuration
response = requests.get(base_url, headers=headers).text

# Extract IMDB identifier and streaming iframe domain from page source
imdb_identifier = re.search(r"src:\s*\'(tt.*?)\'", response).group(1)
stream_domain = re.search(r"AwsIndStreamDomain\s*=\s*\'(.*?)\'", response).group(1)

# Prepare headers for iframe request
iframe_headers = {
    "Referer": stream_domain,
    "Content-type": "application/x-www-form-urlencoded",
    "User-Agent": user_agent
}

# Construct iframe playback URL using extracted IMDB ID
iframe_page_url = f"{stream_domain}play/{imdb_identifier}"

# Request iframe page which contains file endpoint and API key
iframe_html = requests.get(iframe_page_url, headers=iframe_headers).text

# Extract file API endpoint used to retrieve playlist data
file_match = re.search(r'"file":"([^"]+)"', iframe_html)
if not file_match:
    sys.exit("Streaming file endpoint not found")

playlist_api_url = file_match.group(1).replace('\\/', '/')

# Extract CSRF key required for API requests
key_match = re.search(r'"key":"([^"]+)"', iframe_html)
if not key_match:
    sys.exit("API key not found")

csrf_token = key_match.group(1).replace('\\/', '/')

# Attach CSRF token to headers before making API request
iframe_headers['X-CSRF-TOKEN'] = csrf_token

# Request playlist metadata (languages and file references)
playlist_metadata = requests.post(playlist_api_url, headers=iframe_headers).json()

# Resolve actual playlist URLs and collect them with language labels
playlist_results = []
for playlist_entry in playlist_metadata:
    playlist_endpoint = f"{stream_domain}playlist/{playlist_entry['file'].replace('~', '')}.txt"

    playlist_results.append({
        "language": playlist_entry.get("title"),
        "playlist_url": requests.post(playlist_endpoint, headers=iframe_headers).text
    })


# Display extracted playlists
print("\n" + "#" * 25 + "\n" + "#" * 25)

for playlist in playlist_results:
    print(f"\n[{playlist['language']}]: {Colors.okgreen}{playlist['playlist_url']}{Colors.endc}")

print("\n" + "#" * 25 + "\n" + "#" * 25 + "\n")