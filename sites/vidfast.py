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
    "X-Csrf-Token": "afRoMQ0Gulz3cFn3rFpPSwebg8z1Ys5i",
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
static_path = "APA91us-GbhI-Ws6ZInNz-QNV2allAFUx55blgozPyIVI-OeknhulqY61BeJvMaxeSITX9C5UFTQgvQHUiFITaTI3AnEf7DzgWBxay2g6UfwREoc98ACJyz9seVlJC7kWMZEAvPSE32TNk_knj6oB4ayBCXoBTpI7z7uuZuuLbKjM1wWsgr3JKr/c29f50610e7c62617c6311ed5511dabd8003905f/162ec52ba3a977fb9f1fa118af8558615fba46bb9792910a26c598213bb69e0b/b733099d-8cbd-5b16-9a33-76d62e6365d1/q/1000025805044766/vacjeoki"
api_servers = f"https://vidfast.pro/{static_path}/u863YkZdyz8/{servers_token}"
response = requests.post(api_servers, headers=headers).text

# Decrypt servers response
data = {
    'response': response
}
response = requests.post(f'{cf_worker}/decrypt', json=data).json().get('data')

# Select a random server
server = response[1].get('data')
api_stream = f"https://vidfast.pro/{static_path}/Ilz-gRcqmnc/{server}"
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
