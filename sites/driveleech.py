import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs

'''
Supports:
https://driveleech.org/
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
base_url = "https://driveleech.org/file/j1SYy8S6mq"
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
headers = {
    "Referer": "https://driveleech.org",
    "User-Agent": user_agent
}

# Fetch response
response = requests.get(base_url, headers=headers).text
soup = BeautifulSoup(response, 'html.parser')

# Find the anchor tag containing 'Instant Download'
anchor = next((a for a in soup.find_all('a') if "Instant Download" in a.get_text()), None) or sys.exit("Anchor not found")

# Construct API URL and parse encrypted URL
parsed_url = urlparse(anchor['href'])
base_url = f"{parsed_url.scheme}://{parsed_url.netloc}/api"
keys = parse_qs(parsed_url.query).get('url')

# Prepare data and make POST request
data = {
    'keys': keys
}
response = requests.post(base_url, headers=headers, data=data).json()

# Extract video URL
video_url = response['url']

# Print results
print("\n" + "#" * 25 + "\n" + "#" * 25)
print(f"Captured URL: {Colors.okgreen}{video_url}{Colors.endc}")
print("#" * 25 + "\n" + "#" * 25)
print("\n")
