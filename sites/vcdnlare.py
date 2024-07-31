from requests import get, post
from bs4 import BeautifulSoup
import re

base_url = 'https://ww4.vcdnlare.com/v/O2BQzVmy3gZ8BRS'

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

mHeaders = {
    'Referer': 'https://www.5movierulz.tube/',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36'
}

mPageResponse = get(base_url, headers=mHeaders)
mSoup = BeautifulSoup(mPageResponse.text, "html.parser")

mVideoElement = mSoup.find("video", id="player")
if mVideoElement:
    mSourceElement = mVideoElement.find("source")
    if mSourceElement:
        mUrl = mSourceElement.get("src")
        print("\n######################")
        print("######################")
        print(f"Captured URL: {Colors.OKGREEN}{mUrl}{Colors.ENDC}")
        print("######################")
        print("######################\n")
        print(f"\n\n{Colors.WARNING}###This url may not playable with external headers try with https")
    else:
        print("No source element found in the video tag. Try changing referer current referer https://www.5movierulz.bike/")
else:
    print(f"{Colors.FAIL}No video element with id 'player' found.")
