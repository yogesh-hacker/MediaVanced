import requests
import re
from urllib.parse import urlparse, parse_qsl, urlunparse, quote, unquote
import ast
from bs4 import BeautifulSoup

'''
Supports:
https://multiembed.mov/
https://streambucket.com/
https://streamingnow.mov/
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
base_url = "https://multiembed.mov/?video_id=tt0495596"
user_agent = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36"
headers = {
    'Referer': 'https://multiembed.mov',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': user_agent
}

# Utility Functions
''' A Base tranformer '''
def base_transform(d, e, f):
    charset = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ+/"
    g = list(charset)
    h = g[:e]
    i = g[:f]
    j = sum(h.index(b) * (e ** c) for c, b in enumerate(reversed(d)) if b in h)
    k = ""
    while j > 0:
        k = i[j % f] + k
        j = j // f
    return k or 0

''' HUNTER Unpacker '''
def decode_hunter(h, u, n, t, e, r=None):
    r = ""
    i = 0
    while i < len(h):
        s = ""
        while h[i] != n[e]:
            s += h[i]
            i += 1
        i += 1
        for j in range(len(n)):
            s = re.sub(re.escape(n[j]), str(j), s)
        char_code = int(base_transform(s, e, 10)) - t
        r += chr(char_code)
    return unquote(r)


# Get page response and refered page
if 'multiembed' in base_url:
    base_url = requests.get(base_url, headers=headers).url

# Prepare POST data for requesting the page
data = {
    'button-click': 'ZEhKMVpTLVF0LVBTLVF0LVAtMGs1TFMtUXpPREF0TC0wLVYzTi0wVS1RTi0wQTFORGN6TmprLTU=',
    'button-referer': ''
}

# Send POST request to fetch initial response
default_domain = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(base_url))
response = requests.post(base_url, headers=headers, data=data).text

# Extract the session token required to fetch sources
token = re.search(r'load_sources\(\"(.*?)\"\)', response).group(1)

# Request the sources list using the extracted token
response = requests.post("https://streamingnow.mov/response.php", data={"token": token}, headers=headers).text
soup = BeautifulSoup(response, 'html.parser')

# Locate the VIP source
vip_source = soup.find(lambda tag: tag.name == "li" and "vipstream-s" in tag.get_text(strip=True).lower())
if not vip_source:
    exit("No VIP Stream available. Exiting...")

# Extract server and video IDs from the VIP source element
server_id = vip_source.get('data-server')
video_id = vip_source.get("data-id")

# Fetch VIP streaming page HTML
base_url = f"https://streamingnow.mov/playvideo.php?video_id={video_id}&server_id={server_id}&token={token}&init=1"
response = requests.get(base_url, headers=headers).text

# Extract iframe source containing actual video page
soup = BeautifulSoup(response, 'html.parser')
iframe_url = soup.select_one('iframe.source-frame.show')['src']

# Get video page
response = requests.get(iframe_url, headers=headers).text

# Get the encoded HUNTER pack
pattern = re.compile(r'\(\s*function\s*\([^\)]*\)\s*\{.*?\}\s*\(\s*(.*?)\s*\)\s*\)', re.DOTALL)
match = pattern.search(response)
if not match:
    exit(print("Cannot find encoded HUNTER Pack."))

# Decode encoded HUNTER Pack
hunter_pack = match.group(1)
data = ast.literal_eval(hunter_pack)
h,u,n,t,e,r = data[0], data[1], data[2],data[3], data[4], data[5]
decoded_data = decode_hunter(h,u,n,t,e,r)

# Extract video URL
video_match = re.search(r'file:"(https?://[^"]+)"', decoded_data)
video_url = video_match.group(1) if video_match else exit(print("No video URL found."))

# Print results
print("\n" + "#" * 25 + "\n" + "#" * 25)
print(f"Captured URL: {Colors.okgreen}{video_url}{Colors.endc}")
print("#" * 25 + "\n" + "#" * 25)
print(f"{Colors.warning}### Use these headers to access the URL")
print(f"{Colors.okcyan}Referer:{Colors.endc} {default_domain}")
print(f"{Colors.okcyan}User-Agent:{Colors.endc} {user_agent}")
print("\n")