import requests
import re
import sys

'''
Supports:
https://vcloud.lol/
https://hubcloud.dad/
https://reviewsbuddy.in/
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


base_url = "https://hubcloud.bz/drive/oocjo4xi4doj636"
default_domain = "https://hubcloud.bz/"
headers = {
    'Referer': default_domain,
    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36'
}

# Get first page
response = requests.post(base_url, headers=headers).text

# Get next page url
base_match = re.search(r"var\s+url\s*=\s*'(https?:\/\/[^\s]+)'", response)
if not base_match:
    sys.exit(print(f'{Colors.fail}ERROR: Unable to get base URL, make sure file exists{Colors.endc}'))
base_url = base_match.group(1)


# Get next page
response = requests.get(base_url, headers=headers).text

# Extract video URL
video_match = re.search(r"https:\/\/pub[^\s]+", response)
video_url = video_match.group(0).replace("\"", "")

# Print results
print("\n" + "#" * 25 + "\n" + "#" * 25)
print(f"Captured URL: {Colors.okgreen}{video_url}{Colors.endc}")
print("#" * 25 + "\n" + "#" * 25)
print("\n")
