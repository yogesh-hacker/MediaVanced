import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import sys

'''
Supports:
https://send.cm/
https://send.now/
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
base_url = "https://send.now/fbqea2abdm77"
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
parsed_url = urlparse(base_url)
default_domain = f"{parsed_url.scheme}://{parsed_url.netloc}/"
headers = {
    'Referer': default_domain,
    'User-Agent': user_agent
}

# Fetch response
response = requests.get(base_url, headers=headers).text
soup = BeautifulSoup(response, 'html.parser')

# Extract form data and create payload
form = soup.find('form', {'name': 'F1'})
payload = {inp['name']: inp['value'] for inp in form.find_all('input', {'name': True})}

# Extract video URL
response = requests.post(default_domain, headers=headers, data=payload, allow_redirects=False)
video_url = response.headers['Location']

# Print results
print("\n" + "#" * 25 + "\n" + "#" * 25)
print(f"Captured URL: {Colors.okgreen}{video_url}{Colors.endc}")
print("#" * 25 + "\n" + "#" * 25 + "\n")
