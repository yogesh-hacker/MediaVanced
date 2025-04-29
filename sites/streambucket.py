import requests
import re
from urllib.parse import urlparse, parse_qsl, urlunparse, quote, unquote
import ast

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
base_url = "https://multiembed.mov/directstream.php?video_id=tt0495596"
headers = {
    'Referer': 'https://multiembed.mov',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 11) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36'
}

# Utility Functions
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

# Get page response
response = requests.get(base_url, headers=headers).text

# Get the Encoded Hunter Pack
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
raw_video_url = video_match.group(1) if video_match else exit(print("No video URL found."))

# Sanitize URL
parsed_video_url = urlparse(raw_video_url)
raw_query = parsed_video_url.query
params = raw_query.split('&')
encoded_params = '&'.join('='.join(quote(part, safe='') for part in param.split('=', 1))for param in params)
video_url = urlunparse(parsed_video_url._replace(query=encoded_params))

# Print results
print("\n" + "#" * 25 + "\n" + "#" * 25)
print(f"Captured URL: {Colors.okgreen}{video_url}{Colors.endc}")
print("#" * 25 + "\n" + "#" * 25)
print("\n")