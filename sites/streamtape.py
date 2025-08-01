import requests
import re

'''
Supports:
https://streamtape.com/
https://shavetape.cash/
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
base_url = "https://streamtape.com/v/x9vek9lxJ4hDpZ/"
default_domain = "https://streamtape.com/"
initial_headers = {
    'Referer': default_domain,
    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36'
}

# Fetch response
initial_response = requests.get(base_url, headers=initial_headers).text

regex_pattern = r"document\.getElementById\(['\"]captchalink['\"]\)\.innerHTML\s*=\s*['\"]([^'\"]+)['\"].*?\+\s*\(['\"]([^'\"]+)['\"]\)\.substring\(\d+\);"

# Extract video URL
video_match = re.search(regex_pattern, initial_response)
if not video_match:
    exit(print(f'{Colors.fail}ERROR: Streaming URL not found. The video may have been removed.{Colors.endc}'))
video_url = "https:" + video_match.group(1) + video_match.group(2)[4:]

# Print results
print("\n" + "#" * 25 + "\n" + "#" * 25)
print(f"Captured URL: {Colors.okgreen}{video_url}{Colors.endc}")
print("#" * 25 + "\n" + "#" * 25)
print(f"{Colors.warning}### {Colors.bold}Note:{Colors.endc}{Colors.warning} This video URL is valid only for your current IP address.")
print("\n")
