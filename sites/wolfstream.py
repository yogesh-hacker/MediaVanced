import requests
import re

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
    
print(f"\n{Colors.OKCYAN}TARGET: wolfstream.tv{Colors.ENDC}\n{Colors.WARNING}Please use VPN if URL capture fails")

default_domain = "https://wolfstream.tv/"
initial_headers = {
    'Referer': default_domain,
    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36'
}

base_url = "https://wolfstream.tv/hih5xpudhctl/CineDoze.Com-Ganapath_(2023)_MLSBD.Shop-Hindi_HDTVRip_720p.mkv.html"
initial_response = requests.get(base_url, headers=initial_headers)
initial_page_html = initial_response.text

regex_pattern = r'file:"([^"]+)"'
streaming_url_match = re.search(regex_pattern, initial_page_html)

if streaming_url_match:
    streaming_url = streaming_url_match.group(1)
    print("######################")
    print("######################")
    print(f"Captured URL: {Colors.OKGREEN}{streaming_url}{Colors.ENDC}")
    print("######################")
    print("######################\n")
else:
    print(f"{Colors.FAIL}URL not found.{Colors.ENDC}")