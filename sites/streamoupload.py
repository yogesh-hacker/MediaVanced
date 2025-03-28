import requests
import re
from bs4 import BeautifulSoup
import ast

'''
Supports:
https://streamoupload.xyz/
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


base_url = "https://streamoupload.xyz/embed-ycsqt35zobut.html"
user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"

headers = {
    'Referer': "https://streamoupload.xyz/",
    'User-Agent': user_agent,
}

# Fetch the initial response
initial_response = requests.get(base_url, headers=headers).text

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
print(f"{Colors.warning}### Please use the header \"Referer: https://streamoupload.xyz\" or the CDN host to access the URL, along with a User-Agent.\n")
