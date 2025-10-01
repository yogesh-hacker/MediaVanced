import re
import random
import requests
from bs4 import BeautifulSoup

'''
Supports:
https://vcloud.lol/
https://hubcloud.dad/
https://reviewsbuddy.in/
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


base_url = "https://hubcloud.one/drive/vfvuxdwlwicoxno"
default_domain = "https://hubcloud.onr/"
headers = {
    'Referer': default_domain,
    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36'
}

# Get first page
response = requests.post(base_url, headers=headers).text

# Get next page url
match = re.search(r"var\s+url\s*=\s*'(https?:\/\/[^\s]+)'", response)
if not match:
    exit(f'{Colors.fail}ERROR: Unable to get base URL, make sure file exists{Colors.endc}')
file_page = match.group(1)

# Get next page
response = requests.get(file_page, headers=headers).text
soup = BeautifulSoup(response, 'html.parser')

# Parse all file URLs
anchors = soup.find_all('a', class_=lambda c: c and all(cls in c.split() for cls in ['btn', 'btn-lg', 'h6']))
links = []
for anchor in anchors:
    link = anchor.get('href')
    if link:  # make sure href exists
        if ('.mp4' in link or '.mkv' in link) and '.zip' not in link:
            links.append(link)

# Pick a random file URL
video_url = random.choice(links)

# Print results
print("\n" + "#" * 25 + "\n" + "#" * 25)
print(f"Captured URL: {Colors.okgreen}{video_url}{Colors.endc}")
print("#" * 25 + "\n" + "#" * 25)
print("\n")
