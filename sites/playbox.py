import re
import random
import requests
from urllib.parse import urlparse

'''
Supports:
https://nextgencloudfabric.com/
https://vaplayer.ru/
https://vidapi.ru/
https://streamimdb.ru/
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
base_url = 'https://streamimdb.ru/embed/tv/1509/3/2'
user_agent = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"
default_domain = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(base_url))
headers = {
    'Referer': 'https://nextgencloudfabric.com',
    'Origin': 'https://nextgencloudfabric.com',
    'Accept': '*/*',
    'User-Agent': user_agent
}

# Get content info
match = re.search(r'/embed/(\w+)/(\d+)(?:/(\d+)/(\d+))?', base_url)
if match:
    content_type = match.group(1)
    content_id, season, episode = (
        match.group(2),
        match.group(3) or None,
        match.group(4) or None
    )

# Construct the API
api_url = f"https://streamdata.vaplayer.ru/api.php?tmdb={content_id}&type={content_type}"
if content_type != "movie":
    api_url += f"&season={season}&episode={episode}"

# Fetch streaming data
response = requests.get(api_url, headers=headers).json()
streaming_data = response.get('data').get('stream_urls')

# Get video URL
video_url = random.choice(streaming_data)

# Print results
print("\n" + "#" * 25 + "\n" + "#" * 25)
print(f"Captured URL: {Colors.okgreen}{video_url}{Colors.endc}")
print("#" * 25 + "\n" + "#" * 25)
print("\n")
