import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

'''
Supports:
https://gofile.io/
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
base_url = "https://gofile.io/d/xjLcKn"
guest_account_url = "https://api.gofile.io/accounts"
headers = {
    "Access-Control-Request-Headers": "authorization",
    "Access-Control-Request-Method": "GET",
    "Authorization": None
}

# Extract the file ID from the URL
parsed_url = urlparse(base_url)
file_id = parsed_url.path.split('/')[-1]

# Get guest account token
token = None
try:
    response = requests.post(guest_account_url, data={})
    response.raise_for_status()
    response = response.json()
    token = response.get('data', {}).get('token')
    headers['Authorization'] = f'Bearer {token}'
except (requests.RequestException, ValueError) as e:
    exit(print(f"ERROR: {str(e)}"))

# Define the query parameters
params = {"wt": "4fd6sg89d7s6"}
encoded_query = requests.compat.urlencode(params)

# Get file link
response = requests.get(f"https://api.gofile.io/contents/{file_id}?{encoded_query}", headers=headers).json()
children = response.get('data', {}).get('children', {})
if not children:
    raise ValueError("No children found in the response data")

# Extract video URL
first_child_key = list(children.keys())[0]
video_url = children[first_child_key]['link']

# Print results
print("\n" + "#" * 25 + "\n" + "#" * 25)
print(f"Captured URL: {Colors.okgreen}{video_url}{Colors.endc}")
print("#" * 25 + "\n" + "#" * 25)
print(f"{Colors.warning}### Use these headers to access the URL")
print(f"{Colors.okcyan}Cookie: {Colors.endc}accountToken={token}")
print("\n")