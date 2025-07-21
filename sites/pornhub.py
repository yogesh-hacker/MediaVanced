import requests
import re
import json

'''
Supports:
https://www.pornhub.org/
https://www.pornhub.com/
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
base_url = "https://www.pornhub.com/view_video.php?viewkey=67fbdfa54f208"
user_agent = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Mobile Safari/537.36"
headers = {
    "Referer": "https://www.pornhub.org/"
}

# Fetch page content as text
response = requests.get(base_url, headers=headers).text

# Extract JSON-like data from dynamic flashvars variable
match = re.search(r'var\s+flashvars_\d+\s*=\s*({.*?});', response, re.DOTALL)

# Parse matched JSON string to Python dictionary
json_data = json.loads(match.group(1))

# Loop through media definitions and print HLS video URLs with resolution
print("\n" + "#" * 25 + "\n" + "#" * 25)
for video in json_data['mediaDefinitions']:
    if video['format'] == 'hls':
        print(f"{video['height']}p: {Colors.okgreen}{video['videoUrl']}{Colors.endc}")
print("#" * 25 + "\n" + "#" * 25 + "\n")