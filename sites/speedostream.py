import re
import requests
from urllib.parse import urlparse


'''
Supports:
https://speedostream.pm/
https://minoplres.xyz/
https://embdproxy.xyz/
https://spedostream.com/
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
base_url = "https://spedostream.com/embed-l22uzg5bztn5.html"
default_domain = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(base_url))
headers = {
    'Referer': default_domain
}

# Fetch page content
response = requests.get(base_url, headers = headers).text

# Extract video URL
video_url = re.search(r'file:"([^"]+)"', response).group(1)

# Print results
print("\n" + "#" * 25 + "\n" + "#" * 25)
print(f"Captured URL: {Colors.okgreen}{video_url}{Colors.endc}")
print("#" * 25 + "\n" + "#" * 25)
print(f"{Colors.warning}### Use these headers to access the URL")

# Print headers by key: value
print(f"{Colors.okcyan}Referer:{Colors.endc} {default_domain}")
print("\n")