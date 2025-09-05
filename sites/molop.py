import re
import requests
from urllib.parse import urlparse

'''
Supports:
https://molop.art/
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
base_url = 'https://molop.art/watch?v=4XD18PIO'
user_agent = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"
default_domain = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(base_url))
referer_domain = 'https://hdmovie2.institute/' # Provider Domain
headers = {
    'Referer': referer_domain,
    'User-Agent': user_agent
}

# Fetch the webpage content and remove all JavaScript comments
page_content = requests.get(base_url, headers=headers).text
clean_content = re.sub(r'//.*?$|/\*[\s\S]*?\*/', '', page_content, flags=re.MULTILINE)

# Extract the Sniff function arguments
sniff_match = re.search(r'sniff\(([\s\S]*?)\)\s*;', clean_content)
if not sniff_match:
    exit("Error: Unable to locate the Sniff function in the page content.")

# Clean the arguments and split into a list
sniff_args = re.sub(r'[ \n"]+', '', sniff_match.group(1)).split(',')

# Extract the playlist ID and the last parameter (used in the URL)
playlist_id = sniff_args[2]
playlist_token = sniff_args[-1]

# Construct video/playlist URL
video_url = f"https://molop.art/m3u8/1/{playlist_id}/master.txt?s=1&cache=1&plt={playlist_token}"

# Print results
print("\n" + "#" * 25 + "\n" + "#" * 25)
print(f"Captured URL: {Colors.okgreen}{video_url}{Colors.endc}")
print("#" * 25 + "\n" + "#" * 25)
print(f"{Colors.warning}### Note: The playlist can be accessed only a single time!")
print('\n')