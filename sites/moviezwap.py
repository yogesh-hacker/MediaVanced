import re
import random
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, quote

'''
Supports:
https://moviezwap.surf/
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
base_url = 'https://www.moviezwap.surf/movie/Ekka-(2025)-Kannada-Original.html'
user_agent = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"
default_domain = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(base_url))
headers = {
    'Referer': default_domain,
    'User-Agent': user_agent
}

# Fetch page content
response = requests.get(base_url, headers=headers).text
soup = BeautifulSoup(response, 'html.parser')

# Prepare quality dictionary (single value, not list)
qualities = {
    "360p": None,
    "480p": None,
    "720p": None,
    "1080p": None
}

# Find all matching divs
divs = soup.find_all('div', class_='catList')

for div in divs:
    a_tag = div.find('a', href=True)
    
    if a_tag and '?file' in a_tag['href']:
        text = div.get_text(strip=True)
        url = a_tag['href']
        
        # Step 3: Detect quality from text
        for q in qualities.keys():
            if q in text:
                qualities[q] = url   # assign single URL
                break

# Sort qualities by numeric value (highest first)
best_quality = None
best_url = None

for q in sorted(qualities.keys(), key=lambda x: int(x.replace('p', '')), reverse=True):
    if qualities[q]:
        best_quality = q
        best_url = qualities[q]
        break

# Get Download Page
download_url = f"{default_domain}{best_url.replace('/dwload.php', 'download.php')}"
response = requests.get(download_url, headers=headers, allow_redirects=False).text
soup = BeautifulSoup(response, 'html.parser')

# Extract video URL
video_url = None
a_tag = soup.find('a', href=lambda x: x and '.mp4' in x.lower())
if a_tag:
    file_url = a_tag['href']
    video_url = file_url.replace(" ", "%20")

# Print results
# Print Results
print("\n" + "#"*25 + "\n" + "#"*25)
print(f"Captured URL: {Colors.okgreen}{video_url}{Colors.endc}")
print("#"*25 + "\n" + "#"*25)
print(f"{Colors.warning}### Use these headers to access the URL")

# Print headers by key: value
for key, value in headers.items():
    print(f"{Colors.okcyan}{key}:{Colors.endc} {value}")
print("\n")