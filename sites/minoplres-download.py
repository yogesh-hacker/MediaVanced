import requests
from bs4 import BeautifulSoup
import re
import random

base_url = "https://minoplres.xyz/d/4pcxg3uqr9ct_{}"
#https://minoplres.xyz/embed-4pcxg3uqr9ct.html
suffixes = ['h', 'l','o']
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1"
]

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
def generate_random_ip():
    return '.'.join(str(random.randint(0, 255)) for _ in range(4))

headers = {
    "Referer": "https://minoplres.xyz/",
    "X-Forwarded-For": generate_random_ip()
}

for suffix in suffixes:
    url = base_url.format(suffix)
    user_agent = random.choice(user_agents)
    response = requests.get(url, headers=headers)
    print(headers)
    if "This version" not in response.text:
        if "You have to wait" in response.text:
            print("Wait! for "+suffix)
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
