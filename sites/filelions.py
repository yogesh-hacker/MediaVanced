from requests import get, post
from bs4 import BeautifulSoup
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
print(f"\n{Colors.OKCYAN}TARGET: filelions.site{Colors.ENDC}")
mDefaultDomain = "https://filelions.site/"
mTargetUrl = "https://filelions.site/f/j51tar9zz02k"
mHeaders = {
    'Referer': mDefaultDomain
}

mPageResponse = get(mTargetUrl,headers = mHeaders)
mPageHtml = mPageResponse.text
mRegex = r'file:"([^"]+)"'
mMatch = re.search(mRegex, mPageHtml)
if mMatch:
    mUrl = mMatch.group(1)
    print("######################")
    print("######################")
    print(f"Captured URL: {Colors.OKGREEN}{mUrl}{Colors.ENDC}")
    print("######################")
    print("######################\n")
    print(f"\n{Colors.WARNING}###Please use header Referer: {mDefaultDomain} or host to access the url{Colors.ENDC}")
    
else:
    print(f"{Colors.FAIL}URL not found.{Colors.ENDC}")