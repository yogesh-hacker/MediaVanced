# abyss.py
import re
import json
import requests
import cloudscraper
import deobfuscator
from bs4 import BeautifulSoup

## VERSION: 1.2 ##

'''
Supports:
https://abysscdn.com/
https://hydraxcdn.biz/
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
base_url = "https://abysscdn.com/?v=r05GGctsV"
user_agent = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36"
CHARSET = "RB0fpH8ZEyVLkv7c2i6MAJ5u3IKFDxlS1NTsnGaqmXYdUrtzjwObCgQP94hoeW+/="
headers = {
    "Referer": "https://abysscdn.com/",
    "User-Agent": user_agent
}

# Utility Functions
def decode(encoded):
    ''' A Custom Base64 Decoder '''
    charset = "RB0fpH8ZEyVLkv7c2i6MAJ5u3IKFDxlS1NTsnGaqmXYdUrtzjwObCgQP94hoeW+/="
    out = bytearray()
    for i in range(0, len(encoded), 4):
        c = [CHARSET.index(ch) if ch in CHARSET else 64 for ch in encoded[i:i+4].ljust(4, "=")]
        out.append((c[0] << 2) | (c[1] >> 4))
        if c[2] != 64: out.append(((c[1] & 15) << 4) | (c[2] >> 2))
        if c[3] != 64: out.append(((c[2] & 3) << 6) | c[3])
    return out.decode("utf-8", "ignore")

# Initialize Cloudscraper session (bypasses Cloudflare)
scraper = cloudscraper.create_scraper()

# Fetch and parse webpage content
response = scraper.get(base_url).text
soup = BeautifulSoup(response, 'html.parser')

# Locate target script and deobfuscate its contents
script_elements = soup.find_all('script')
script_obfuscated = script_elements[7].text
deobfuscated = deobfuscator.deobfuscate(script_obfuscated)

# Extract and decode main metadata
encoded = re.search(r"[a-zA-Z]=\'(.*?)_\'", deobfuscated).group(1)
metadata = json.loads(decode(encoded))

# Extract additional metadata values
metadata['id'] = re.search(r"\[\'id\'\]=\'(edns.*?)\'", deobfuscated).group(1)
metadata['slug'] = re.search(r"\[\'slug\'\]=\'(.*?)\'", deobfuscated).group(1)
metadata['md5_id'] = re.search(r"\[\'md5_id\'\]=(\d+)", deobfuscated).group(1)
metadata['domain'] = re.search(r"\[\'domain\'\]=\'(.*?)\'", deobfuscated).group(1)

# Display metadata and constructed video URL
print(f'\n{Colors.okgreen}METADATA:{Colors.endc} {metadata}')
print(f"\nCaptured URL: {Colors.okgreen}https://{metadata['domain']}/{metadata['id']}\n")
print(f"{Colors.warning}### You may need additional set-up to play these video URLs. Thank You!{Colors.endc}\n")
