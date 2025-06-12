import re
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

'''
Supports:
https://darkibox.com/
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
base_url = 'https://darkibox.com/0u3sfm76wqpc'
user_agent = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"
default_domain = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(base_url))
headers = {
    "Referer": default_domain,
    "Content-Type": 'application/x-www-form-urlencoded',
    'Accept': '*/*',
    "User-Agent": user_agent
}
session = requests.Session()

# Fetch page content
response = session.get(base_url, headers=headers).text
soup = BeautifulSoup(response, 'html.parser')

# Get form input values
form = soup.select_one('form')
inputs = form.find_all('input')
data = {}
for input in inputs:
    data[input['name']] = input['value']

# Post Data Contents after 3 Seconds
time.sleep(3)
response = session.post(base_url, headers=headers, data=data).text

# Extract video URL
match = re.search(r'sources:\s*\[\{src:\s*\"(.*?)\"', response)
video_url = match.group(1)

# Print results
print("\n" + "#" * 25 + "\n" + "#" * 25)
print(f"Captured URL: {Colors.okgreen}{video_url}{Colors.endc}")
print("#" * 25 + "\n" + "#" * 25)
print("\n")