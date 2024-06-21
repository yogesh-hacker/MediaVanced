import requests
import re
from bs4 import BeautifulSoup
from js2py import EvalJs
import warnings

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

def ignore_user_warnings(message, category, filename, lineno, file=None, line=None):
    return category == UserWarning
warnings.showwarning = ignore_user_warnings

base_url = "https://streambucket.net/vipstream2.php?token=STJXUVNTS0dsNE5ZaDhISkRSOTFIVzd0VS92Q3JBdkZQNnFoNFVNcms4S0psenBNeTJCam1FenNrWG41VGlOc0pmSUo="
default_domain = "https://streambucket.net/"
print(f"\n{Colors.OKCYAN}TARGET: {default_domain}{Colors.ENDC}")
print(f"\n{Colors.WARNING}Caution: Please note that URLs from {default_domain} using tokens for streaming links may expire after some time.{Colors.ENDC}")

try:
    session = requests.Session()

    initial_headers = {
        "Referer": "https://vidsrc.net/",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"
    }
    initial_response = session.get(base_url, headers=initial_headers)
    initial_response.raise_for_status()  # Raise an error for bad response status

    initial_page_html = initial_response.text
    soup = BeautifulSoup(initial_page_html, "html.parser")
    script = soup.find_all("script")
    
    # Assuming script[1] exists and has string attribute
    decrypt_script = script[1].string.replace("eval(function", "function decode").replace("(escape(r))}(", "(escape(r))}var decodedString = decode(")
    final_script = decrypt_script[:-1]

    context = EvalJs()
    context.execute(final_script)
    decoded_string = context.decodedString

    pattern = r'file:"(https?://[^"]+)"'
    match = re.search(pattern, decoded_string)
    
    if match:
        stream_url = match.group(1)
        print("######################")
        print("######################")
        print(f"Captured URL: {Colors.OKGREEN}{stream_url}{Colors.ENDC}")
        print("######################")
        print("######################\n")
    else:
        print(f"{Colors.FAIL}URL not found.{Colors.ENDC}")

except requests.RequestException as e:
    print(f"{Colors.FAIL}Error during request: {e}{Colors.ENDC}")

except (IndexError, AttributeError) as e:
    print(f"{Colors.FAIL}Error parsing script: {e}{Colors.ENDC}")

except Exception as e:
    print(f"{Colors.FAIL}An unexpected error occurred: {e}{Colors.ENDC}")
