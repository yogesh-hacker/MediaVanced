import requests
from bs4 import BeautifulSoup
import json
import re
import ast

'''
Supports:
https://streamwish.to/
https://rapidplayers.com/
https://moflix-stream.click/
https://dhtpre.com/
https://vidhide.com/
https://mixdrop.ps/
https://multimovies.cloud/
https://hlsflex.com/
https://ghbrisk.com/
https://niikaplayerr.com/
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

base_url = "https://hlsflex.com/e/d2hs3drp40pw"
headers = {
    'User-Agent':'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36'
}


initial_response = requests.get(base_url, headers=headers).text

initial_regex = r'file:"([^"]+)"'
initial_match = re.search(initial_regex, initial_response)

# Fetch and parse the initial response
soup = BeautifulSoup(initial_response, 'html.parser')
js_code = next((script.string for script in soup.find_all('script') if script.string and "eval(function(p,a,c,k,e,d)" in script.string), "")

# Extract and clean the JS code
encoded_packed = re.sub(r"eval\(function\([^\)]*\)\{[^\}]*\}\(|.split\('\|'\)\)\)", '', js_code)
data = ast.literal_eval(encoded_packed)

# Base-36 conversion helper function
def to_base_36(n):
    return '' if n == 0 else to_base_36(n // 36) + "0123456789abcdefghijklmnopqrstuvwxyz"[n % 36]

# Extract values from packed data
p, a, c, k = data[0], int(data[1]), int(data[2]), data[3].split('|')

# Replace placeholders with corresponding values
for i in range(c):
    if k[c - i - 1]:
        p = re.sub(r'\b' + to_base_36(c - i - 1) + r'\b', k[c - i - 1], p)

#Get Video URL
video_url = re.search(r'file:"([^"]+)', p).group(1)

# Print Results
print("\n" + "#"*25 + "\n" + "#"*25)
print(f"Captured URL: {Colors.okgreen}{video_url}{Colors.endc}")
print("#"*25 + "\n" + "#"*25)
print(f"{Colors.warning}### Please use the header \"Referer: https://rapidplayers.com\" or the CDN host to access the URL, along with a User-Agent.\n")
