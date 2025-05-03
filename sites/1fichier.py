import requests
from bs4 import BeautifulSoup
import re
import urllib3

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

'''
Supports:
https://1fichier.com/
'''

# The site has SSL and IP verification measures, so the scraper may not always work reliably.

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
base_url = "https://1fichier.com/?8j23awpf2mp93xq04bui&af=62851"
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
af_value = re.search(r"af=(\d+)", base_url).group(1) if "af=" in base_url else "0"

headers = {
    "Referer": "https://1fichier.com",
    "User-Agent": user_agent
}

cookies = {
    "AF": af_value
}

# Set up session
session = requests.Session()
session.headers.update(headers)
session.cookies.update(cookies)


# Fetch response
response = session.get(base_url, verify=False).text
soup = BeautifulSoup(response, "html.parser")

# Extract and POST data
adz = soup.find("input", attrs = {"name":"adz"})['value']
payload = {
    "adz" : adz
}
response = session.post(base_url, data=payload, verify=False).text

# Extract video url
soup = BeautifulSoup(response, "html.parser")
video_link = soup.find("a", attrs={"class": "ok btn-general btn-orange"})

if video_link is None:
    print(f"{Colors.warning}The site has detected security issues. Please try again with a different IP or use a proxy. Exiting...{Colors.endc}")
    exit(1)

video_url = video_link['href']

# Print results
print("\n" + "#" * 25 + "\n" + "#" * 25)
print(f"Captured URL: {Colors.okgreen}{video_url}{Colors.endc}")
print("#" * 25 + "\n" + "#" * 25)
print("\n")
