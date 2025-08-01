import re
import json
import html
import requests
from urllib.parse import urlparse

''' A Scraper module for KickAssAnime '''

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
user_agent = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"

# Utilities
def get_domain(url):
    domain = '{uri.scheme}://{uri.netloc}'.format(uri=urlparse(url))
    return domain

# Fetch page content
def real_extract(url):
    # Initialize required configs
    headers = {
        "Referer": get_domain(url),
        "User-Agent": user_agent
    }
    
    # Fetch initial page
    response = requests.get(url, headers=headers).text
    
    # Get data
    data = re.search(r'props=\"(.*?)\"', response).group(1)
    decoded_data = json.loads(html.unescape(data))
    
    # Return video URL
    video_url = decoded_data['manifest'][1]
    return f'https:{video_url}'