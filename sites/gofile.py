import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

guest_account_url = "https://api.gofile.io/accounts"
base_url = "https://gofile.io/d/0aiagU"

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
print(f"\n{Colors.OKCYAN}TARGET: gofile.io{Colors.ENDC}")

# Extract the file ID from the URL
parsed_url = urlparse(base_url)
file_id = parsed_url.path.split('/')[-1]

# Fetch guest account token
try:
    guest_account_response = requests.post(guest_account_url, data={})
    guest_account_response.raise_for_status()
    guest_account_data = guest_account_response.json()
    token = guest_account_data.get('data', {}).get('token')
    if not token:
        raise ValueError("Failed to fetch guest account token")
except (requests.RequestException, ValueError) as e:
    print("\n######################")
    print("######################")
    print(f"Error fetching guest account token: {e}")
    print("######################")
    print("######################\n")
    exit()

# Prepare headers for fetching file link
fetch_params = {"wt": "4fd6sg89d7s6"}
query_string = requests.compat.urlencode(fetch_params)
headers = {
    "Access-Control-Request-Headers": "authorization",
    "Access-Control-Request-Method": "GET",
    "Authorization": f"Bearer {token}"
}

# Fetch file link
try:
    content_data_response = requests.get(f"https://api.gofile.io/contents/{file_id}?{query_string}", headers=headers)
    content_data_response.raise_for_status()
    content_data = content_data_response.json()
    children = content_data.get('data', {}).get('children', {})
    if not children:
        raise ValueError("No children found in the response data")
    first_child_key = list(children.keys())[0]
    link = children[first_child_key]['link']
    print("######################")
    print("######################")
    print(f"Captured URL: {Colors.OKGREEN}{link}{Colors.ENDC}")
    print("######################")
    print("######################\n")
    headers2 ={
        "Cookie":"accountToken=8SmVDp6PVW1CdkUIfOl8VvLHgp1bp9nZ"
    }
    print(requests.get(link,headers=headers2).headers)
except (requests.RequestException, ValueError) as e:
    print("\n######################")
    print("######################")
    print(f"Error fetching file link: {e}")
    print("######################")
    print("######################\n")
