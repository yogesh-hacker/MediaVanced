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
    
print(f"\n{Colors.OKCYAN}TARGET: streamtape.com{Colors.ENDC}")

default_domain = "https://streamtape.com/"
initial_headers = {
    'Referer': default_domain,
    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36'
}

base_url = "https://streamtape.com/v/x9vek9lxJ4hDpZ/"
initial_response = requests.get(base_url, headers=initial_headers)
initial_page_html = initial_response.text

regex_pattern = r"document\.getElementById\(['\"]captchalink['\"]\)\.innerHTML\s*=\s*['\"]([^'\"]+)['\"].*?\+\s*\(['\"]([^'\"]+)['\"]\)\.substring\(\d+\);"
print(regex_pattern)
botlink_match = re.search(regex_pattern, initial_page_html)

if botlink_match:
    streaming_url = "https:" + botlink_match.group(1) + botlink_match.group(2)[4:]
    print("######################")
    print("######################")
    print(f"Captured URL: {Colors.OKGREEN}{streaming_url}{Colors.ENDC}")
    print("######################")
    print("######################\n")
else:
    print(f"{Colors.FAIL}ERROR: Unable to locate streaming URL{Colors.ENDC}")
