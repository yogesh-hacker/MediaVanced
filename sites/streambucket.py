import requests
import re
from urllib.parse import urlparse, unquote


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


base_url = "https://multiembed.mov/directstream.php?video_id=tt12735488"
headers = {
    'Referer': "https://multiembed.mov/",
    'User-Agent': 'Mozilla/5.0 (Linux; Android 11) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36'
}

def base_convert(n, f, t, c="0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ+/"):
    d, r = int(n, f), ""
    while d: r = c[d % t] + r; d //= t
    return r or "0"

def decode_hunter(h, u, n, t, e, r):
    e = int(e)
    t = int(t)
    r = ""
    i = 0
    while i < len(h):
        s = ""
        while h[i] != n[e]:
            s += h[i]
            i += 1
        for j in range(len(n)):
            s = re.sub(n[j], str(j), s)
        decoded_value = int(base_convert(s, e, 10)) - t
        r += chr(decoded_value)
        i += 1

    return unquote(r)

# Get page response
initial_response = requests.get(base_url, headers=headers)
default_domain = f"https://{urlparse(initial_response.url).hostname}/"
initial_response = initial_response.text

# Get and decode hunter pack
pattern = r'eval\(function\((.*?)\)\{.*\}\((.*?)\)\)'
hunter_pack_match = re.search(pattern, initial_response)

decoded_js =""
if hunter_pack_match:
    hunter_pack = hunter_pack_match.group(2).replace("\"", "").split(',')
    decoded_js = decode_hunter(*hunter_pack)
else:
    print("Failed to extract hunter pack.")


# Extract video URL
video_match = re.search(r'file:"(https?://[^"]+)"', decoded_js)
video_url = video_match.group(1) if video_match else exit(print("No video URL found."))

# Print results
print("\n" + "#" * 25 + "\n" + "#" * 25)
print(f"Captured URL: {Colors.okgreen}{video_url}{Colors.endc}")
print("#" * 25 + "\n" + "#" * 25)
print(f"{Colors.warning}### Use these headers to access the URL")
