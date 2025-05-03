import requests
from base64 import b64decode
import random
import time
import re
import os
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

## Library v4.4 ##

'''
Supports:
https://vidstreamnew.xyz/
https://moviesapi.club/
https://chillx.top/
https://boosterx.stream/
https://playerx.stream/
https://vidstreaming.xyz/
https://raretoonsindia.co/
https://plyrxcdn.site/
https://newer.stream/
https://mov18plus.cloud/
'''

# @PlayerX, Nice choice with Diffie-Hellman! 🔐
# At this point, you're not even a security challenge... you're just my warm-up exercise.
# Keep trying, maybe one day you’ll at least trigger my firewall.
# 23rd attempt at cracking you—haha! 💥😂
# Contact: businesshackerindia@gmail.com 📧

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
base_url = "https://mov18plus.cloud/v/Ozovj52rRSj2/"
user_agent = "Mozilla/5.0 (Linux; Android 11; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"
headers = {
    "Referer": "https://mov18plus.cloud",
    "User-Agent": user_agent
}

# Utility Functions
# Generate a 12-byte random hex nonce
def get_nonce():
    random_float = random.random()
    x = base36_encode(int(str(random_float).split('.')[1]))
    z = base36_encode(int(time.time() * 1000))
    return x + z

def base36_encode(num):
    chars = '0123456789abcdefghijklmnopqrstuvwxyz'
    if num == 0:
        return '0'
    result = ''
    while num > 0:
        num, i = divmod(num, 36)
        result = chars[i] + result
    return result


def mod_exp(base, exp, mod):
    base = int(base)
    exp = int(exp)
    mod = int(mod)
    result = 1

    while exp > 0:
        if exp & 1:
            result = (result * base) % mod
        base = (base * base) % mod
        exp >>= 1
    return result

# Set Up Session for all requests(Optional)
session = requests.Session()
session.headers.update(headers)

# Fetch page and extract encrypted data
response = session.get(base_url).text
match = re.search(r"(?:const|let|var|window\.\w+)\s+\w*\s*=\s*'(.*?)'", response)
if not match:
    exit(print("No encrypted data found."))

encrypted_data = match.group(1)

# Generate client's key pair
dh_modulus = int("0xFFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA237327FFFFFFFFFFFFFFFF", 16)
generator = 2
random_bytes_hex = os.urandom(32).hex()
client_private_key = int(random_bytes_hex, 16) % dh_modulus
client_public_key = mod_exp(generator, client_private_key, dh_modulus)

# ----------- #
# ----------- #

# Step 1: Prepare token by sending public key and nonce
data = {
    "nonce": get_nonce(),
    "client_public": str(client_public_key)
}

response = session.post("https://raretoonsindia.co/api-2/prepair-token.php", json=data).json()

# Get necessary data
pre_token = response['pre_token']
csrf_token = response['csrf_token']
server_public = response['server_public']

# ----------- #
# ----------- #

# Step 2: Request access token using pre_token and csrf
initial_nonce = get_nonce()
data = {
    "nonce": initial_nonce,
    "pre_token": pre_token,
    "csrf_token": csrf_token
}

response = session.post("https://raretoonsindia.co/api-2/create-token.php", json=data).json()

access_token = response['token']

# ----------- #
# ----------- #

# Step 3: Send encrypted data with required tokens
data = {
    "token": access_token,
    "initial_nonce": initial_nonce,
    "nonce": get_nonce(),
    "csrf_token": csrf_token,
    "pre_token": pre_token,
    "encrypted_data": encrypted_data
}

response = session.post("https://raretoonsindia.co/api-2/last-process.php", json=data).json()

# Step 4: Derive shared key using server public key and client's private key
shared_secret = mod_exp(server_public, client_private_key, dh_modulus)
derived_key = SHA256.new(str(shared_secret).encode()).digest()

# Step 5: Get encrypted data from response
encrypted_data = b64decode(response['encrypted_result'])
iv = b64decode(response['iv'])
hmac = b64decode(response['hmac'])
temp_iv = b64decode(response['temp_iv'])
encrypted_symmetric_key = b64decode(response['encrypted_symmetric_key'])

# Step 6: Decrypt the encrypted symmetric key using the derived key and temporary IV
symmetric_key_cipher = AES.new(derived_key, AES.MODE_CBC, iv=temp_iv)
padded_symmetric_key = symmetric_key_cipher.decrypt(encrypted_symmetric_key)
actual_aes_key = unpad(padded_symmetric_key, AES.block_size)

# Step 7: Decrypt the actual encrypted payload using the real AES key and original IV
payload_cipher = AES.new(actual_aes_key, AES.MODE_CBC, iv)
padded_decrypted_payload = payload_cipher.decrypt(encrypted_data)

# Step 8: Unpad and decode the decrypted data to get the final readable result
decrypted_payload = unpad(padded_decrypted_payload, AES.block_size)
decrypted_data = decrypted_payload.decode("utf-8")

# Extract video URL
video_match = re.search(r'(?:file\s*:\s*|"file"\s*:\s*)"(https?://[^"]+)"', decrypted_data)
video_url = video_match.group(1) if video_match else exit(print("No video URL found."))

# Print results
print("\n" + "#" * 25 + "\n" + "#" * 25)
print(f"Captured URL: {Colors.okgreen}{video_url}{Colors.endc}")
print("#" * 25 + "\n" + "#" * 25)
print(f"{Colors.warning}### Use these headers to access the URL")

# Print headers by key: value
for key, value in headers.items():
    print(f"{Colors.okcyan}{key}:{Colors.endc} {value}")
print("\n")
