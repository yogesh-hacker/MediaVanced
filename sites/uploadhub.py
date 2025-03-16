import requests
import re
import os
from bs4 import BeautifulSoup

'''
Supports:
https://uploadhub.wf/
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

base_url = "https://uploadhub.wf/0ze9m65exlci"

default_domain = "https://www.uploadhub.wf/"
session = requests.Session()

headers = {
    "Referer": base_url,
    "User-Agent":"Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"
}

# Get first page
initial_response = session.get(base_url, headers=headers)
soup = BeautifulSoup(initial_response.text, "html.parser")

# Get form data
op = soup.find("input", attrs = {"name":"op"})['value']
file_id = soup.find("input", attrs = {"name":"id"})['value']
random = soup.find("input", attrs = {"name":"rand"})['value']
referer = soup.find("input", attrs = {"name":"referer"})['value']

payload = {
    "op": op,
    "adblock": "0",
    "id": file_id,
    "method_free": "",
    "referer": referer,
    "method_premium": ""
}

# Post the data
initial_response = session.post(initial_response.url, data=payload, headers=headers).text
soup = BeautifulSoup(initial_response,"html.parser")

# Extract video URL
video_url = soup.find("div", attrs = {"id":"direct_link"}).find("a")['href']

# Print results
print("\n" + "#" * 25 + "\n" + "#" * 25)
print(f"Captured URL: {Colors.okgreen}{video_url}{Colors.endc}")
print("#" * 25 + "\n" + "#" * 25)
print("\n")
