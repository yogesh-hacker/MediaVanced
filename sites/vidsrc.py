import requests
import re
import json
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import hashlib
import struct
import os
import math
from urllib.parse import urlparse, unquote
from bs4 import BeautifulSoup


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


def decode_url(enc_type: str, url: str) -> str | None:
    if enc_type == "NdonQLf1Tzyx7bMG":
        return bMGyx71TzQLfdonN(url)
    elif enc_type == "sXnL9MQIry":
        return Iry9MQXnLs(url)
    elif enc_type == "IhWrImMIGL":
        return IGLImMhWrI(url)
    elif enc_type == "xTyBxQyGTA":
        return GTAxQyTyBx(url)
    elif enc_type == "ux8qjPHC66":
        return C66jPHx8qu(url)
    elif enc_type == "eSfH1IRMyL":
        return MyL1IRSfHe(url)
    elif enc_type == "KJHidj7det":
        return detdj7JHiK(url)
    elif enc_type == "o2VSUnjnZl":
        return nZlUnj2VSo(url)
    elif enc_type == "Oi3v1dAlaM":
        return laM1dAi3vO(url)
    elif enc_type == "TsA2KGDGux":
        return GuxKGDsA2T(url)
    elif enc_type == "JoAHUMCLXV":
        return LXVUMCoAHJ(url)
    else:
        return None

def bMGyx71TzQLfdonN(a: str) -> str:
    b = 3
    c = []
    d = 0
    while d < len(a):
        c.append(a[d:d + b])
        d += b
    e = ''.join(c[::-1])
    return e

def Iry9MQXnLs(a: str) -> str:
    b = "pWB9V)[*4I`nJpp?ozyB~dbr9yt!_n4u"
    d = ''.join([chr(int(a[i:i+2], 16)) for i in range(0, len(a), 2)])
    c = ''.join([chr(ord(d[i]) ^ ord(b[i % len(b)])) for i in range(len(d))])
    e = ''.join([chr(ord(ch) - 3) for ch in c])
    return base64.b64decode(e).decode('utf-8')

def IGLImMhWrI(a: str) -> str:
    b = a[::-1]
    c = ''.join(
        chr(ord(it) + 13) if 'a' <= it <= 'm' or 'A' <= it <= 'M' else 
        chr(ord(it) - 13) if 'n' <= it <= 'z' or 'N' <= it <= 'Z' else it 
        for it in b
    )
    d = c[::-1]
    return base64.b64decode(d).decode('utf-8')

def C66jPHx8qu(a: str) -> str:
    b = a[::-1]
    c = "X9a(O;FMV2-7VO5x;Ao\x05:dN1NoFs?j,"
    d = ''.join([chr(int(b[i:i+2], 16)) for i in range(0, len(b), 2)])
    e = ''.join([chr(ord(d[i]) ^ ord(c[i % len(c)])) for i in range(len(d))])
    return e

def MyL1IRSfHe(a: str) -> str:
    b = a[::-1]
    c = ''.join([(chr(ord(it) - 1)) for it in b])
    d = ''.join([chr(int(c[i:i+2], 16)) for i in range(0, len(c), 2)])
    return d

def laM1dAi3vO(a: str) -> str:
    b = a[::-1]
    c = b.replace("-", "+").replace("_", "/")
    d = base64.b64decode(c).decode('utf-8')
    e = ''.join([chr(ord(ch) - 5) for ch in d])
    return e

def detdj7JHiK(a: str) -> str:
    b = a[10:len(a) - 16]
    c = "3SAY~#%Y(V%>5d/Yg\"$G[Lh1rK4a;7ok"
    d = base64.b64decode(b).decode('utf-8')
    e = (c * ((len(d) + len(c) - 1) // len(c)))[:len(d)]
    f = ''.join([chr(ord(d[i]) ^ ord(e[i])) for i in range(len(d))])
    return f

def GTAxQyTyBx(a: str) -> str:
    b = a[::-1]
    c = ''.join([b[i] for i in range(len(b)) if i % 2 == 0])
    return base64.b64decode(c).decode('utf-8')

def LXVUMCoAHJ(a: str) -> str:
    b = a[::-1]
    c = b.replace("-", "+").replace("_", "/")
    d = base64.b64decode(c).decode('utf-8')
    e = ''.join([chr(ord(ch) - 3) for ch in d])
    return e

def GuxKGDsA2T(a: str) -> str:
    b = a[::-1]
    c = b.replace("-", "+").replace("_", "/")
    d = base64.b64decode(c).decode('utf-8')
    e = ''.join([chr(ord(ch) - 7) for ch in d])
    return e

base_url = "https://vidsrc.in/embed/movie/tt10698680"
headers = {
    'Referer': "https://vidsrc.in/",
    'User-Agent': 'Mozilla/5.0 (Linux; Android 11) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36'
}

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re

# Step 1: Fetch the initial response and parse the iframe source
initial_response = requests.get(base_url, headers=headers).text
soup = BeautifulSoup(initial_response, 'html.parser')
iframe_src = soup.find('iframe', attrs={'id': 'player_iframe'})['src']

# Step 2: Fetch the iframe content and determine the default domain
iframe_response = requests.get(f"https:{iframe_src}", headers=headers)
default_domain = f"https://{urlparse(iframe_response.url).hostname}"

# Step 3: Extract the script source using regex
pattern = r"src:\s*'([^']+)'"
match = re.search(pattern, iframe_response.text)
final_url = f"{default_domain}{match.group(1)}" if match else ''

# Step 4: Fetch the final response and decode the hidden content
if final_url:
    final_response = requests.get(final_url, headers=headers)
    soup = BeautifulSoup(final_response.text, 'html.parser')
    
    encoded_element = soup.find('div', attrs={'style': 'display:none;'})
    encoded = encoded_element.text
    encoding_type = encoded_element['id']
    
    print("\n######################")
    print("######################")
    print(f"Captured URL: {Colors.okgreen}{decode_url(encoding_type, encoded)}{Colors.endc}")
    print("######################")
    print("######################\n")
else:
    print(f"{Colors.fail}Final URL not found!{Colors.endc}")