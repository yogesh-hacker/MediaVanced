import requests
import re
import os
from bs4 import BeautifulSoup
import os
from pathlib import Path
import base64


class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

default_domain = "https://saicord.com/"
print(f"\n{Colors.OKCYAN}TARGET: {default_domain}{Colors.ENDC}")
session = requests.Session()
initial_headers = {
    "Referer": default_domain,
    "User-Agent":"Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"
}

cookies = {
    "cf_clearance" : "7EMvhCoJXzLoB95qoypKRxLaPwEPPMQ_lxNTrZXUgHg-1718419969-1.0.1.1-MDMXbyRum_hdlG34Ovqctc_8sHoWFCS1PMa1xp17Rwydf_uZWwRYnKdeTUprNRxfkExtOm6K_rJPxHzeKOc4KQ"
}

base_url = "https://saicord.com/hi/movies/1433-attack-on-finland.html"
initial_response = requests.get(base_url,headers=initial_headers,cookies=cookies)
initial_page_html = initial_response.text
soup = BeautifulSoup(initial_page_html,"html.parser")
iframe = soup.find("div", attrs={"class": "player-iframe"})
script = iframe.find_all("script")
pattern = r'atob\("([^"]*)"\)'
matcher = re.search(pattern, script[1].string)
if matcher:
    encoded_data = matcher.group(1);
    decoded_bytes = base64.b64decode(encoded_data)
    decoded_string = decoded_bytes.decode('utf-8')
    pattern = r'file:"([^"]+)"'
    matcher = re.search(pattern, decoded_string)
    if matcher:
        print("######################")
        print("######################")
        print(f"Captured URL: {Colors.OKGREEN}{matcher.group(1)}{Colors.ENDC}")
        print("######################")
        print("######################\n")