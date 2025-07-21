import re
import base64
import requests
import cloudscraper
from bs4 import BeautifulSoup

'''
Supports:
https://saicord.com/
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
base_url = "https://saicord.com/hi/movies/1433-attack-on-finland.html"
default_domain = "https://saicord.com/"
headers = {
    "Referer": default_domain,
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"
}

cookies = {
    "cf_clearance" : "Y8doFuh8iHDmeTtx2BcymH_XUdwUg2rbT7ebwRTmMsQ-1722687625-1.0.1.1-32h0KLviCUYW48bTf3GzGn5MgqW9GMlNCo2t28iFRzW3y2aTMQeLq_iMtmteV4GpfqzpMI.7E1ww6jWGofoRIw"
}

# Create Cloudscraper Session to bypass Cloudflare
scraper = cloudscraper.create_scraper()

# Fetch response
response = scraper.get(base_url, headers=headers, cookies=cookies).text
soup = BeautifulSoup(response,"html.parser")

# Get main script
iframe = soup.find("div", attrs={"class": "player-iframe"})
script = iframe.find_all("script")

encrypted_data_match = re.search(r'atob\("([^"]*)"\)', script[1].string)
if not encrypted_data_match:
    exit(print("No encrypted data found."))

# Decode encrypted data
encoded_data = encrypted_data_match.group(1);
decoded_bytes = base64.b64decode(encoded_data)
decoded_string = decoded_bytes.decode('utf-8')

# Extract video URL
video_match = re.search(r'file:"([^"]+)"', decoded_string)
video_url = video_match.group(1) if video_match else exit(print("No video URL found."))

# Print results
print("\n" + "#" * 25 + "\n" + "#" * 25)
print(f"Captured URL: {Colors.okgreen}{video_url}{Colors.endc}")
print("#" * 25 + "\n" + "#" * 25)
print("\n")
