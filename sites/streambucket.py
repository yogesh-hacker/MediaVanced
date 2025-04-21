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

# Constants
base_url = "https://multiembed.mov/directstream.php?video_id=tt12735488"
headers = {
    'Referer': 'https://multiembed.mov',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 11) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36'
}

# Get page response
response = requests.get(base_url, headers=headers).text

# Extract video URL
video_match = re.search(r'file:"(https?://[^"]+)"', response)
video_url = video_match.group(1) if video_match else exit(print("No video URL found."))

# Print results
print("\n" + "#" * 25 + "\n" + "#" * 25)
print(f"Captured URL: {Colors.okgreen}{video_url}{Colors.endc}")
print("#" * 25 + "\n" + "#" * 25)
print("\n")