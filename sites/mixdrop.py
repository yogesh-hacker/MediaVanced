import re
import ast
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

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
base_url = "https://mixdrop21.net/e/9n9vml60u33qp1d"
user_agent = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36"
default_domain = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(base_url))
headers = {
    'Referer': default_domain,
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

# Fetch the initial response
base_url = base_url.replace('/f/', '/e/')
response = requests.get(base_url, headers=headers).text

# Packed data pattern
pattern = r'eval\(function\((.*?)\)\{.*\}\((.*?)\)\)'
data_match = re.search(pattern, response)

# Extract packed data if found
data = ""
if data_match:
    data = data_match.group(2).replace(".split('|')", "");
    data = ast.literal_eval(data)
else:
    exit(f"{Colors.fail}Error: Cannot find packed data. File might be deleted. Exiting...{Colors.endc}")

# Extract variables from packed data
p,a,c,k,e,d = data[0], int(data[1]), int(data[2]), data[3].split('|'), 0, {}

# Replace function to decode the packed data
decoded_data = unpack(p,a,c,k,e,d)

# Regex to find the video URL
regex_match = re.search(r'MDCore\.wurl=\"(.*?)\"', decoded_data)

# Get video URL
video_url = ""
if regex_match:
    video_url = f"https:{regex_match.group(1)}"
else:
    print(f"{Colors.fail}Video URL not found!{Colors.endc}")

# Print Results
print("\n" + "#"*25 + "\n" + "#"*25)
print(f"Captured URL: {Colors.okgreen}{video_url}{Colors.endc}")
print("#"*25 + "\n" + "#"*25)
print(f"{Colors.warning}### Use these headers to access the URL")

# Print headers by key: value
for key, value in headers.items():
    print(f"{Colors.okcyan}{key}:{Colors.endc} {value}")
print("\n")