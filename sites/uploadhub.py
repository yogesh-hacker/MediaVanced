import requests
import re
import os
from bs4 import BeautifulSoup

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

base_url = "http://uploadhub.wf/2o4zyfqa07qh"

default_domain = "https://www.uploadhub.wf/"
print(f"\n{Colors.OKCYAN}TARGET: {default_domain}{Colors.ENDC}")
session = requests.Session()


initial_headers = {
    "Referer": base_url,
    "User-Agent":"Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"
}

initial_response = session.get(base_url,headers=initial_headers)
initial_page_html = initial_response.text
soup = BeautifulSoup(initial_page_html,"html.parser")
op = soup.find("input", attrs = {"name":"op"})['value']
file_id = soup.find("input", attrs = {"name":"id"})['value']
random = soup.find("input", attrs = {"name":"rand"})['value']
referer = soup.find("input", attrs = {"name":"referer"})['value']

payload = {
    "op":op,
    "adblock":"0",
    "id":file_id,
    "method_free":"",
    "referer":referer,
    "method_premium":""
}

initial_response = session.post(initial_response.url, data=payload, headers=initial_headers)
initial_page_html = initial_response.text
soup = BeautifulSoup(initial_page_html,"html.parser")
download_url = soup.find("div", attrs = {"id":"direct_link"}).find("a")['href']
print("######################")
print("######################")
print(f"Captured URL: {Colors.OKGREEN}{download_url}{Colors.ENDC}")
print("######################")
print("######################\n")