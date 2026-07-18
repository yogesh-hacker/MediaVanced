import random
import base64
import requests
from Crypto.Cipher import AES
from urllib.parse import urlparse, quote


'''
Supports:
https://vidrock.net/
https://vidrock.ru/
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
base_url = "https://vidrock.ru/movie/533535/"
user_agent = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36"
default_domain = '{uri.scheme}://{uri.netloc}'.format(uri=urlparse(base_url))
aes_key_hex = "7f3e9c2a8b5d1f4e6a9c3b7d2e5f8a1c4b6d9e2f5a8c1b4d7e9f2a5c8b1d4e7f"
headers = {
    "Referer": default_domain,
    "User-Agent": user_agent,
}

# Extract path from base url
slug = urlparse(base_url).path

# Get streaming info
response = requests.get(f'{default_domain}/api/{slug}').json()

# Pick a random valid server
server = random.choice([s for s in response.values() if s.get("url")])

# Decode the Base64URL payload and extract the AES-GCM components.
encrypted_payload = server["url"]
encrypted_data = base64.urlsafe_b64decode(
    encrypted_payload + "=" * (-len(encrypted_payload) % 4)
)

nonce = encrypted_data[:12]
ciphertext = encrypted_data[12:-16]
auth_tag = encrypted_data[-16:]

# Decrypt and authenticate the encrypted stream URL using AES-256-GCM.
cipher = AES.new(bytes.fromhex(aes_key_hex), AES.MODE_GCM, nonce=nonce)
stream_url = cipher.decrypt_and_verify(ciphertext, auth_tag).decode("utf-8")

# Get video URL
video_url = stream_url

# Print results
print("\n" + "#" * 25 + "\n" + "#" * 25)
print(f"Captured URL: {Colors.okgreen}{video_url}{Colors.endc}")
print("#" * 25 + "\n" + "#" * 25)
print(f"{Colors.warning}### Use these headers to access the URL")
print(f"{Colors.okcyan}Referer:{Colors.endc} {default_domain}")
print(f"{Colors.okcyan}User-Agent:{Colors.endc} {user_agent}")
print("\n")
