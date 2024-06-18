import requests
from bs4 import BeautifulSoup
import re

base_url = "https://minoplres.xyz/d/0hc5f76a6tk1_{}"

suffixes = ['h', 'l','o']

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
print(f"\n{Colors.OKCYAN}TARGET: minoplres.xyz{Colors.ENDC}")

headers = {
    "Referer": "https://minoplres.xyz/"
}

for suffix in suffixes:
    url = base_url.format(suffix)
    response = requests.get(url, headers=headers)
    
    if "This version" not in response.text:
        mPageHtml = response.text
        mSoup = BeautifulSoup(mPageHtml,"html.parser")
        mOp = mSoup.find("input", attrs = {"name": "op"})
        mId = mSoup.find("input", attrs = {"name":"id"})
        mMode = mSoup.find("input", attrs = {"name":"mode"})
        mHash = mSoup.find("input", attrs = {"name":"hash"})
        
        payload = {
            "op": mOp['value'],
            "id": mId['value'],
            "mode": mMode['value'],
            "hash": mHash['value']
        }
        
        mResponse2 = requests.post(url, data=payload, headers=headers)
        mPageHtml2 = mResponse2.text
        mPattern = r'href="([^"]+\.mp4[^"]*)"'
        mMatch = re.search(mPattern, mPageHtml2)
        if mMatch:
            print("######################")
            print("######################")
            print(f"Captured URL: {Colors.OKGREEN}{mMatch.group(1)}{Colors.ENDC}")
            print("######################")
            print("######################\n")
    else:
        print(f"{Colors.FAIL}Request to {url} failed because: QUALITY UNAVAILABLE{Colors.ENDC}")
