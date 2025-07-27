import re
import ast
import json
import requests
from urllib.parse import urlparse

'''
Supports:
https://x.pixfusion.in/
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
base_url = 'https://x.pixfusion.in/video/d26b10ca0de48de1619fcefc39d00d64'
user_agent = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"
default_domain = '{uri.scheme}://{uri.netloc}'.format(uri=urlparse(base_url))
headers = {
    'Referer': default_domain,
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': user_agent
}

# Utility Functions
''' JS Unpacker '''
def unpack(p, a, c, k, e=None, d=None):
    digits = "0123456789abcdefghijklmnopqrstuvwxyz"
    def base_encode(n):
        rem = n % a
        digit = chr(rem + 29) if rem > 35 else digits[rem]
        if n < a:
            return digit
        return base_encode(n // a) + digit

    d = {} if d is None else d
    for i in range(c - 1, -1, -1):
        key = base_encode(i)
        d[key] = k[i] if i < len(k) and k[i] else key

    pattern = re.compile(r'\b\w+\b')
    def replace(m):
        w = m.group(0)
        return d.get(w, w)

    return pattern.sub(replace, p)

# Fetch page content
response = requests.get(base_url, headers=headers).text

# Packed data pattern
pattern = r'eval\(function\((.*?)\)\{.*\}\((.*?)\)\)'
data_match = re.search(pattern, response)

# Extract packed data if found
data = None
if data_match:
    data = data_match.group(2).replace(".split('|')", "")
    data = ast.literal_eval(data)
else:
    print("Failed to extract packed data.")

# Extract variables from packed data
p,a,c,k,e,d = data[0], int(data[1]), int(data[2]), data[3].split('|'), 0, {}

# Unpack packed data
decoded_data = unpack(p,a,c,k,e,d).replace('\\', '')

# Get Video ID and Source
video_id = re.search(r'FirePlayer\(\"(.*?)\"', decoded_data).group(1)
data = {
    'hash': video_id,
    'r': ''
}
response = requests.post(f'{default_domain}/player/index.php?data={video_id}&do=getVideo', headers=headers, data=data).json()

# Extract video URL
video_url = response['videoSource']

# Print results
print("\n" + "#" * 25 + "\n" + "#" * 25)
print(f"Captured URL: {Colors.okgreen}{video_url}{Colors.endc}")
print("#" * 25 + "\n" + "#" * 25)
print(f"{Colors.warning}### Use these headers to access the URL")

# Print headers by key: value
print(f"{Colors.okcyan}Referer:{Colors.endc} {default_domain}/")
print("\n")