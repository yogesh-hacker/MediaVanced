import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

'''
Supports:
https://vidsrc.to/
https://vidsrc.xyz/
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
base_url = "https://vidsrc.to/embed/movie/tt24517830"
user_agent = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36"
default_domain = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(base_url))
headers = {
    "Referer": default_domain,
    "User-Agent": user_agent,
}

# Fetch page content
response = requests.get(base_url, headers=headers).text
soup = BeautifulSoup(response, 'html.parser')

# Get actual iframe page
rcp_iframe = soup.select_one("#player_iframe")
if not rcp_iframe:
    base_url = base_url.replace('.to', '.xyz')
    soup = BeautifulSoup(requests.get(base_url, headers=headers).text, 'html.parser')
    rcp_iframe = f'https:{soup.select_one("#player_iframe")['src']}'
else:
    rcp_iframe = f'https:{rcp_iframe['src']}'

# Get prorcp iframe
response = requests.get(rcp_iframe, headers=headers).text
default_domain = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(rcp_iframe))
prorcp_iframe = re.search(r"src:\s'(.*?)'", response).group(1)

# Get final iframe
final_iframe = f'{default_domain}{prorcp_iframe}'
response = requests.get(final_iframe, headers=headers).text

# Extract video URL
headers['Referer'] = default_domain
video_url = re.search(r"file:\s'(.*?)'", response).group(1)

# Print results
print("\n" + "#" * 25 + "\n" + "#" * 25)
print(f"Captured URL: {Colors.okgreen}{video_url}{Colors.endc}")
print("#" * 25 + "\n" + "#" * 25)
print(f"{Colors.warning}### Use these headers to access the URL")

# Print headers by key: value
for key, value in headers.items():
    print(f"{Colors.okcyan}{key}:{Colors.endc} {value}")
print("\n")
