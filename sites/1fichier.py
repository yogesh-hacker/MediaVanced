import requests
import re
import os
from bs4 import BeautifulSoup
import os
from pathlib import Path
import base64
from js2py import EvalJs
import binascii
import codecs
import time

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

base_url = "https://1fichier.com/?vqi59hurbe20vlu5f7jx"
default_domain = "https://1fichier.com/"
print(f"\n{Colors.OKCYAN}TARGET: {default_domain}{Colors.ENDC}")
session = requests.Session()


initial_headers = {
    "Referer": base_url,
    "User-Agent":"Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"
}

initial_response = session.get(base_url,headers=initial_headers)
initial_page_html = initial_response.text
soup = BeautifulSoup(initial_page_html, "html.parser")
adz = soup.find("input", attrs = {"name":"adz"})['value']
payload = {
    "adz" : adz
}
initial_response = session.post(base_url, data=payload,headers=initial_headers)
initial_page_html = initial_response.text
soup = BeautifulSoup(initial_page_html, "html.parser")
error = soup.find("div", attrs={"class": "ct_warn"})
if error and 'wait' in error.text:
    error_text = ' '.join(error.text.split())
    time = re.search(r'(\d+)\s+minutes', error_text, re.IGNORECASE).group(1)
    print("######################")
    print("######################")
    print(f"{Colors.FAIL}ERROR: This website enforces a timer between downloads. Please wait {time} minutes.{Colors.ENDC}")
    print(f"{Colors.OKCYAN}Solution: To bypass the timer, change your IP between requests.{Colors.ENDC}")
    print("######################")
    print("######################\n")
else:
    download_url = soup.find("a", attrs={"class": "ok btn-general btn-orange"})['href']
    print("######################")
    print("######################")
    print(f"Captured URL: {Colors.OKGREEN}{download_url}{Colors.ENDC}")
    print("######################")
    print("######################\n")
