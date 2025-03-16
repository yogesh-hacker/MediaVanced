import requests
import re
from bs4 import BeautifulSoup
import base64

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
    "cf_clearance" : "7EMvhCoJXzLoB95qoypKRxLaPwEPPMQ_lxNTrZXUgHg-1718419969-1.0.1.1-MDMXbyRum_hdlG34Ovqctc_8sHoWFCS1PMa1xp17Rwydf_uZWwRYnKdeTUprNRxfkExtOm6K_rJPxHzeKOc4KQ"
}

# Fetch response
initial_response = requests.get(base_url, headers=headers, cookies=cookies).text
soup = BeautifulSoup(initial_response,"html.parser")

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
