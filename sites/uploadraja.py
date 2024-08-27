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
    
def save_file_in_internal_directory(filename, content, directory='/storage/emulated/0'):
    file_path = os.path.join(directory, filename)
    try:
        with open(file_path, 'w') as file:
            file.write(content)
        print(f"File saved to {file_path}")
    except Exception as e:
        print(f"Error saving file: {e}")

def hex_to_char(match):
    return chr(int(match.group(1), 16))

base_url = "https://uploadraja.com/f/aa230b-4qynkmytwota3"

default_domain = "https://uploadraja.com/"
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
random = soup.find("input", attrs = {"name":"rand"})['value']
file_id = soup.find("input", attrs = {"name":"id"})['value']
referer = soup.find("input", attrs = {"name":"referer"})['value']
table_data = soup.find("td", attrs = {"align":"right"})
span_texts = [span.get_text() for span in table_data.find_all('span')]
captcha_text = ''.join(span_texts)
payload = {
    "op": op,
    "rand": random,
    "id": file_id,
    "adblock_detected" : "0",
    "code": captcha_text,
    "referer": base_url,
    "method_premium": "",
    "method_free": "Slow Download"
}

print(f"{Colors.WARNING}Can't skip countdown please wait 15 Seconds...!{Colors.ENDC}")
# Try to bypass Wrong Captcha Detection!
initial_response = session.head(base_url, headers=initial_headers)
time.sleep(15)
initial_response = session.post(base_url, data=payload, headers=initial_headers)
initial_page_html = initial_response.text
soup = BeautifulSoup(initial_page_html,"html.parser")
error = soup.find("div", attrs={"class":"err"})
if error:
    print(f"{Colors.FAIL}ERROR: {error.text} detected!{Colors.ENDC}")
else:
    download_url = soup.find("a",attrs={"class","downloadbtn"})['href']
    print("######################")
    print("######################")
    print(f"Captured URL: {Colors.OKGREEN}{download_url}{Colors.ENDC}")
    print("######################")
    print("######################\n")