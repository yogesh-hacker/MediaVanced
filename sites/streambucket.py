import requests
import re
from urllib.parse import urlparse, unquote

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

def base_convert(number_str, from_base, to_base):
    charset = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ+/"
    
    from_base_chars = charset[:from_base]
    to_base_chars = charset[:to_base]

    decimal_value = sum(
        from_base_chars.index(char) * (from_base ** index)
        for index, char in enumerate(reversed(number_str))
        if char in from_base_chars
    )

    if decimal_value == 0:
        return "0"

    converted_value = ""
    while decimal_value > 0:
        converted_value = to_base_chars[decimal_value % to_base] + converted_value
        decimal_value //= to_base
    return converted_value

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


base_url = "https://multiembed.mov/directstream.php?video_id=tt12735488"
headers = {
    'Referer': "https://multiembed.mov/",
    'User-Agent': 'Mozilla/5.0 (Linux; Android 11) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36'
}

raw_initial_response = requests.get(base_url, headers=headers)
default_domain = f"https://{urlparse(raw_initial_response.url).hostname}/"
initial_response = raw_initial_response.text

pattern = r'eval\(function\((.*?)\)\{.*\}\((.*?)\)\)'
hunter_pack_match = re.search(pattern, initial_response)

decoded_js =""
if hunter_pack_match:
    hunter_pack = hunter_pack_match.group(2).replace("\"", "").split(',')
    decoded_js = decode_hunter(*hunter_pack)
else:
    print("Failed to extract hunter pack.")

pattern = r'file:"(https?://[^"]+)"'
match = re.search(pattern, decoded_js)
if match:
    stream_url = match.group(1)
    print("\n######################")
    print("######################")
    print(f"Captured URL: {Colors.okgreen}{stream_url}{Colors.endc}")
    print("######################")
    print("######################")
    print(f"{Colors.warning}### Please use the header Referer: {default_domain} or the CDN host to access the URL, along with a User-Agent.\n")
else:
    print(f"{Colors.fail}URL not found.{Colors.endc}")