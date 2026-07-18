import re
import requests
from urllib.parse import urlparse

'''
Supports:
https://vidup.to/
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
base_url = "https://vidup.to/movie/587412"
user_agent = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36"
default_domain = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(base_url))
cf_worker = "https://vidup.yogeshkumarjamre1.workers.dev"
headers = {
    "Accept": "*/*",
    "Referer": default_domain,
    "User-Agent": user_agent,
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

# Get route config
response = requests.get(f'{cf_worker}/route-config').json()
data = response.get('data', {})
static_path, server_path, stream_path = (
    data.get('static_path'),
    data.get('server_path'),
    data.get('stream_path')
)
api_headers = response.get('headers')


# Generate payload
data = {
    'siteData': raw_data
}
response = requests.post(f'{cf_worker}/generate', json=data).json()
servers_token = response.get('payload')

# Get streaming servers
api_servers = f"https://vidup.to/{static_path}/{server_path}/{servers_token}"
response = requests.post(api_servers, headers=api_headers).text

# Decrypt servers response
data = {
    'response': response
}
response = requests.post(f'{cf_worker}/decrypt', json=data).json().get('data')

# Select a random server
server = response[0].get('data')
api_stream = f"https://vidup.to/{static_path}/{stream_path}/{server}"
response = requests.post(api_stream, headers=api_headers).text

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
