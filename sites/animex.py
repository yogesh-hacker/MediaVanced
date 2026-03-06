import re
import os
import json
import time
import base64
import random
import requests
from Crypto.Cipher import AES
from urllib.parse import urlparse

'''
Supports:
https://animex.one/
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
base_url = 'https://animex.one/watch/your-name-21519-episode-1'
user_agent = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"
aes_key_hex = "0153a09e3ac652d285f7ca21505ee3b3a2820965136fb4dc9c9190069641190e"
primary_key_hex = "a6d74d826a2effed042741d60611657165fcfdf0cccaea1345842d4c520f11cd0ebe2a4374d849f34fab2904e99e472d03e3310882a746b3d3a99815ffe60764"
secondary_key_hex = "2657e6804e386e99dc27a6ecb0085f6715992feea8e1b9e8c6754a9ea0db806946e015a2dc17d9630e8ed62947d8e6fc"
lookup_table_hex = "9e0b6e267d4e72da1d13698d828d5c266cc641287844a6e8a64fc3f0932f33e5e410ee6d82710c0ec79b3d57eb003ca7fa62a311dfed075dd18fc8215a48ad33f50d43e25543710a0af25623afab61d8823a8b923d77d9f2a88b3e9521702b28d2bad56fc699753069686c3e349b7387b559a0d887d4d79e78922d666fcebfd310b532fc638732e1d01d0972cf2130974dae542a0e55385cb75899cf4e86a1142efaa89c7bc1af1a1562c337f2a9a5668b07ce05aeedf82412f32699b1b6863593a1967d654fd6a60b9ba3701b3aa76a5805ff8e0231e92fb9ed0c8431b149180e77ea564ef6b0e8b188afe14842f603f7c65666a6fc528462ca2b2e7c13b632"
default_domain = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(base_url))
headers = {
    'Referer': default_domain,
    'User-Agent': user_agent
}

# Utility Functions
'''XOR each byte with static keys, a lookup table, and a position-based constant. '''
def xor_diffuse_bytes(input_bytes: bytes, key1: bytes, key2: bytes, lookup_table: bytes) -> bytes:
    output_bytes = bytearray(len(input_bytes))
    
    for i, byte in enumerate(input_bytes):
        # Pick values from key1 with offsets
        key1_val1 = key1[i % len(key1)]
        key1_val2 = key1[(i + 7) % len(key1)]
        key1_val3 = key1[(i + 13) % len(key1)]
        
        # Pick values from key2 with offsets
        key2_val1 = key2[i % len(key2)]
        key2_val2 = key2[(i + 11) % len(key2)]
        
        # Lookup from global table
        table_val = lookup_table[(i * 7) % 256]
        
        # XOR everything + position-dependent constant
        output_bytes[i] = (byte ^ key1_val1 ^ key1_val2 ^ key1_val3 ^ key2_val1 ^ key2_val2 ^ table_val ^ (i * 23)) & 0xFF

    return bytes(output_bytes)

''' Swap nibbles and XOR each byte with a position-based mask. '''
def swap_nibbles_and_mask(input_bytes: bytes) -> bytes:
    output = bytearray(len(input_bytes))
    for index, byte in enumerate(input_bytes):
        mask = (index * 23) & 0xFF
        output[index] = ((byte << 4 | byte >> 4) & 0xFF) ^ mask
    return bytes(output)

# Get content info
content_info = re.search(r'\/.*?(\d+)-episode-(\d+)', base_url)
media_id = content_info.group(1)
episode_num = content_info.group(2)

# Prepare payload for encryption
payload = {
    "id": int(media_id),
    "host": "pahe",
    "epNum": episode_num,
    "type": "sub",
    "cache": "true",
    "timestamp": int(time.time() * 1000)
}
plaintext = json.dumps(payload)

# Scramble plaintext bytes with nibble swap and mask
payload_bytes = plaintext.encode("utf-8")
scrambled_bytes = swap_nibbles_and_mask(payload_bytes)

# Diffuse scrambled bytes using static keys and lookup table
lookup_table_bytes = bytes.fromhex(lookup_table_hex)
primary_key_bytes = bytes.fromhex(primary_key_hex)
secondary_key_bytes = bytes.fromhex(secondary_key_hex)
diffused_bytes = xor_diffuse_bytes(scrambled_bytes, primary_key_bytes, secondary_key_bytes, lookup_table_bytes)

# Convert hex keys to bytes for AES-GCM
aes_key_bytes = bytes.fromhex(aes_key_hex)
iv_bytes = os.urandom(12)

# Encrypt with AES-256-GCM
cipher = AES.new(aes_key_bytes, AES.MODE_GCM, nonce=iv_bytes)
ciphertext, tag = cipher.encrypt_and_digest(diffused_bytes)

# Combine IV + ciphertext + tag
encrypted_blob = iv_bytes + ciphertext + tag

# Encode URL-Safe and Get streaming data
encoded = base64.urlsafe_b64encode(encrypted_blob).decode().rstrip("=")
stream_info = requests.get(f'{default_domain}/api/anime/sources/{encoded}', headers=headers).json()

# Parse video URL
video_url = stream_info.get('sources')[0].get('url')

# Print Results
print("\n" + "#"*25 + "\n" + "#"*25)
print(f"Captured URL: {Colors.okgreen}{video_url}{Colors.endc}")
print("#"*25 + "\n" + "#"*25)
print(f"{Colors.warning}### Use these headers to access the URL")

# Print headers by key: value
for key, value in headers.items():
    print(f"{Colors.okcyan}{key}:{Colors.endc} {value}")
print("\n")
