import requests
import re
import sys
import json

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
base_url = "https://noodlemagazine.com/watch/-227654991_456239224"
user_agent = "Mozilla/5.0 (Linux; Android 11; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"
headers = {
    'Referer': base_url,
    'User-Agent': user_agent
}

# Fetch the initial response
response = requests.get(base_url, headers=headers).text

# Regex to extract the JSON part
match = re.search(r'window\.playlist\s*=\s*({.*?});', response, re.DOTALL)

json_data = ""
if match:
    playlist_json = match.group(1)
    try:
        json_data = json.loads(playlist_json)
    except json.JSONDecodeError as e:
        print("JSON Decode Error:", e)
else:
    print("window.playlist not found")

qualities = json_data['sources']

divider = "#" * 25
print(f"\n{divider}\n{divider}")
for quality in qualities:
    print(f"{Colors.bold}{quality['label']}p{Colors.endc}: {Colors.okgreen}{quality['file']}{Colors.endc}")
print(f"{divider}\n{divider}\n")