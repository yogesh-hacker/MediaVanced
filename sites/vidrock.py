import random
import base64
import numbers
import requests
from urllib.parse import urlparse


'''
Supports:
https://vidrock.net/
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
base_url = "https://vidrock.net/movie/533535"
user_agent = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36"
default_domain = '{uri.scheme}://{uri.netloc}'.format(uri=urlparse(base_url))
headers = {
    "Referer": default_domain,
    "User-Agent": user_agent,
}

# Utility Functions
def numbers_to_text(numbers: str) -> str:
    """Converts numbers to letters (0–25)"""
    result = []
    for digit in numbers:
        if digit.isdigit():
            ch = chr(int(digit) + ord('a'))
            result.append(ch)
    return "".join(result)

# Extract and reverse item ID from base URL
isMovie = True
if 'movie' in base_url:
    item_id = base_url.split('/')[-1][::-1]
else:
    segs = base_url.split('/')
    item_id = f"{segs[-1]}-{segs[-2]}-{segs[-3][::-1]}"

# Double Base64 encode item_id
item_type = "tv"
if isMovie:
    item_type = "movie"
    item_id = numbers_to_text(item_id)
encoded = base64.b64encode(item_id.encode()).decode()
encoded = base64.b64encode(encoded.encode()).decode()

# Get streaming info
response = requests.get(f'{default_domain}/api/{item_type}/{encoded}').json()

# Load all valid sources
sources = []
for src in response.values():
    if src.get('url'):
        sources.append(src['url'])

# Pick a random video URL
video_url = random.choice(sources)

# Print results
print("\n" + "#" * 25 + "\n" + "#" * 25)
print(f"Captured URL: {Colors.okgreen}{video_url}{Colors.endc}")
print("#" * 25 + "\n" + "#" * 25)
print("\n")