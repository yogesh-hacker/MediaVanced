import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urlparse
import re
import json 
import json

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
base_url = "https://www.dailymotion.com/player/metadata/video/x8qqe3e"
default_domain = "https://www.dailymotion.com/"
initial_headers = {
    'Referer': default_domain,
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36'
}
session = requests.Session()

# Get page response
initial_response = session.get(base_url, headers=initial_headers)
json_content = initial_response.json()

video_url = json_content["qualities"]["auto"][0]["url"]

# Print results
print("\n" + "#" * 25 + "\n" + "#" * 25)
print(f"Captured URL: {Colors.okgreen}{video_url}{Colors.endc}")
print("#" * 25 + "\n" + "#" * 25)
print("\n")