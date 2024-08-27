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
import warnings


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
    
def ignore_user_warnings(message, category, filename, lineno, file=None, line=None):
    return category == UserWarning
warnings.showwarning = ignore_user_warnings

base_url = "https://mixdrop.ms/e/eno3x81kt94le8"

default_domain = "https://mixdrop.ms/"
print(f"\n{Colors.OKCYAN}TARGET: {default_domain}{Colors.ENDC}")
session = requests.Session()


initial_headers = {
    "Referer": base_url,
    "User-Agent":"Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"
}

initial_response = session.get(base_url,headers=initial_headers)
initial_page_html = initial_response.text
pattern = 'eval\(function\(p,a,c,k,e,d\)\{.*?\}\)'
match = re.search(pattern, initial_page_html)
function_code = match.group(0).replace("eval(function","function hello").replace("return p}(","return p} var download_link=hello(")
context = EvalJs()
context.execute(function_code)
decoded_string = context.download_link
pattern = r'MDCore\.wurl="([^"]+)"'
match = re.search(pattern, decoded_string)
download_url = "https:"+match.group(1)
print("######################")
print("######################")
print(f"Captured URL: {Colors.OKGREEN}{download_url}{Colors.ENDC}")
print("######################")
print("######################\n")
