import requests
import re
from bs4 import BeautifulSoup
import sys

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

base_url = "https://mixdrop.sb/e/k0lo0mlqapx47o"
user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"

headers = {
    'Referer': "https://mixdrop.sb/",
    'User-Agent': user_agent
}

# Utility Functions
# Base-36 conversion helper function
def to_base_36(n):
    return '' if n == 0 else to_base_36(n // 36) + "0123456789abcdefghijklmnopqrstuvwxyz"[n % 36]

# Replace placeholders with corresponding values
def unpack(p,a,c,k,e,d):
    for i in range(c):
        if k[c - i - 1]:
            p = re.sub(r'\b' + to_base_36(c - i - 1) + r'\b', k[c - i - 1], p)
    return p

# Fetch the initial response
response = requests.get(base_url, headers=headers).text

# Fetch and parse the initial response
soup = BeautifulSoup(response, 'html.parser')
script_content = next((script.text for script in soup.find_all('script') if "mxcontent" in script.text), "")
if not script_content:
    sys.exit(f"{Colors.fail}Error: Cannot find a valid script. It might be deleted. Exiting...{Colors.endc}")

# Packed data pattern
pattern = r'eval\(function\((.*?)\)\{.*\}\((.*?)\)\)'
data_match = re.search(pattern, script_content)

# Extract packed data if found
data = ""
if data_match:
    data = data_match.group(2).replace("\"", "").replace(".split('|')", "").replace("\'","").split(',')
else:
    print("Failed to extract packed data.")

# Extract variables from packed data
p,a,c,k,e,d = data[0], int(data[1]), int(data[2]), data[3].split('|'), int(data[4]), {}

# Replace function to decode the packed data
decoded_data = unpack(p,a,c,k,e,d)

# Regex to find the video URL
regex_match = re.search(r"MDCore\.wurl=([^;]+)", decoded_data)

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
print(f"{Colors.warning}### Please use the header \"Referer: https://mixdrop.sb/\" or the CDN host to access the URL, along with a User-Agent.\n")