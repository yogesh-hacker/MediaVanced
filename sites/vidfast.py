import re
import requests
from urllib.parse import urlparse

'''
Supports:
https://vidfast.pro/
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
base_url = "https://vidfast.pro/movie/533535"
user_agent = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36"
default_domain = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(base_url))
cf_worker = "https://vidfast.yogeshkumarjamre1.workers.dev"
headers = {
    "Accept": "*/*",
    "Referer": default_domain,
    "User-Agent": user_agent,
    "X-Csrf-Token": "qSisdq0Eza7t9Ja9DmH5sEq376Kv0Oom",
    "X-Requested-With": "XMLHttpRequest"
}

''' Due to the complexity and size of the encryption workflow, 
the implementation has been moved to the backend. 
If you require access to the backend code, please contact me on Discord. '''


# Fetch page content
response = requests.get(base_url, headers=headers).text

# Extract raw data
match = re.search(r'\\"en\\":\\"(.*?)\\"', response)
if not match:
    exit(print("No data found!"))
raw_data =  match.group(1)

# Generate payload
data = {
    'siteData': raw_data
}
response = requests.post(f'{cf_worker}/generate', json=data).json()
servers_token = response.get('payload')

# Get streaming servers
static_path = "segucow/1000051563617990/1fd3effe9c35dd1a5d26627c1e21c98db2d8489b4cbdb7fe7530006d07586afc/APA913f6aqvxI-1XWSPgcpTvD7pjmh--az_4XJCmB_CPZt3VqhurjM5tE3WFr3WxoWhwsSNXfj_flz0pcq_DV8SiBvA5ZAO_FN97LKe1HJLxXXisFO_Ps5Wv55lRrDRlos9Y8KsQrLXJbTUIHaJK8HqMwJA1fD692JsZ6FnqUR5B1Mc47ug05Lz/ze"
api_servers = f"https://vidfast.pro/{static_path}/DwJsWR1VHKg/{servers_token}"
response = requests.post(api_servers, headers=headers).text

# Decrypt servers response
data = {
    'response': response
}
response = requests.post(f'{cf_worker}/decrypt', json=data).json().get('data')

# Select a random server
server = response[0].get('data')
api_stream = f"https://vidfast.pro/{static_path}/-Wm0yYBQuCE/{server}"
response = requests.post(api_stream, headers=headers).text

# Decrypt stream response
data = {
    'response': response
}
response = requests.post(f'{cf_worker}/decrypt', json=data).json().get('data')

# Extract video URL
video_url = response.get('url')

# Print results
print("\n" + "#" * 25 + "\n" + "#" * 25)
print(f"Captured URL: {Colors.okgreen}{video_url}{Colors.endc}")
print("#" * 25 + "\n" + "#" * 25)
print(f"{Colors.warning}### Use these headers to access the URL")
print(f"{Colors.okcyan}Referer:{Colors.endc} {default_domain}")
print("\n")
