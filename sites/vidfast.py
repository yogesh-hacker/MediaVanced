import re
import time
import base64
import hashlib
import requests
from Crypto.Cipher import AES
from urllib.parse import urlparse
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes

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
aes_key = bytes.fromhex("50bb6a529bfb4abb1969c1a29c8cac6df1f00ec63a7297c4c06dcc9473cdacc4")
aes_iv = bytes.fromhex("ffe7765f45669a794181d0b4a8d9e96b")
xor_seed_key = bytes.fromhex("1a5d66c3fbf2")
headers = {
    "Accept": "*/*",
    "Referer": default_domain,
    "User-Agent": user_agent,
    "X-Csrf-Token": "22Xg4bhHnx4uUolyJWs7rdNBbIzYVz8z",
    "X-Requested-With": "XMLHttpRequest"
}

# Utility Functions
''' Encodes input using Base64 with custom character mapping. '''
def custom_encode(input_bytes):
    source_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_"
    target_chars = "4jrpDdPNYKMiBLgwczuHGksmOIoS2-JVRCnbfl769A0UeE5Qyt_aWq1xTF3vhXZ8"
    translation_table = str.maketrans(source_chars, target_chars)
    encoded = base64.urlsafe_b64encode(input_bytes).decode().rstrip('=')
    return encoded.translate(translation_table)

'''Generate a KSA-like permutation from a hash seed'''
def generate_ksa(seed, size):
    s = seed if isinstance(seed, bytes) else bytes(seed)
    state = (int.from_bytes(s[0:4],"little") ^ int.from_bytes(s[4:8],"little") ^
             int.from_bytes(s[8:12],"little") ^ int.from_bytes(s[12:16],"little")) & 0xffffffff

    S = list(range(size))
    for i in range(size-1, 0, -1):
        state ^= (state << 13) & 0xffffffff
        state ^= state >> 17
        state ^= (state << 5) & 0xffffffff
        state &= 0xffffffff
        j = state % (i+1)
        S[i], S[j] = S[j], S[i]
    return S

'''Rotate and mask a byte using a key'''
def transform_byte(input_byte, key_byte):
    r = key_byte % 8
    rotated = ((input_byte << r) | (input_byte >> (8 - r))) & 0xff
    return (rotated + (key_byte ^ 0xA5)) & 0xff

'''Shuffles the payload into blocks according to the permutation box'''
def shuffle_blocks(payload, pbox):
    payload_len = len(payload)
    num_blocks = len(pbox)

    if payload_len % num_blocks != 0:
        raise ValueError(f"Payload length ({payload_len}) must be divisible by pbox length ({num_blocks})")

    block_size = payload_len // num_blocks
    result = bytearray(payload_len)

    for dst_idx, src_block in enumerate(pbox):
        src_start = src_block * block_size
        dst_start = dst_idx * block_size
        result[dst_start:dst_start + block_size] = payload[src_start:src_start + block_size]

    return result

# Fetch page content
response = requests.get(base_url, headers=headers).text

# Extract raw data
match = re.search(r'\\"en\\":\\"(.*?)\\"', response)
if not match:
    exit(print("No data found!"))
raw_data =  match.group(1)

# Get timestamp bytes
timestamp_bytes = bytearray(8)
timestamp = int(time.time() * 1000)
for i in range(8):
        timestamp_bytes[i] = timestamp & 255
        timestamp >>= 8

# Prepare Input
random_iv = get_random_bytes(16)
site_buffer = raw_data.encode()
combined_input = random_iv + timestamp_bytes + site_buffer

# PKCS7 padding
pad = 16 - len(combined_input) % 16
combined_input += bytes([pad]) * pad

# Encrypt
cipher = AES.new(aes_key, AES.MODE_CBC, aes_iv)
encrypted = cipher.encrypt(combined_input)
encrypted_bytes = bytearray(encrypted)

# Step 1 XOR
xor_seed = xor_seed_key + random_iv
xor_hash = hashlib.sha256(xor_seed).digest()
xor_output = bytearray(len(encrypted_bytes))

for i in range(len(encrypted_bytes)):
    if i > 0 and i % len(xor_hash) == 0:
        xor_hash = hashlib.sha256(xor_hash).digest()
    xor_output[i] = encrypted_bytes[i] ^ xor_hash[i % len(xor_hash)]

# Step 2 Byte Transform
transform_seed = aes_key + random_iv
transform_hash = hashlib.sha256(transform_seed).digest()
transform_output = bytearray(len(xor_output))
for i in range(len(xor_output)):
    transform_output[i] = transform_byte(xor_output[i], transform_hash[i % len(transform_hash)])

# Step 3 KSA
ksa_seed = random_iv + xor_seed_key + aes_iv
ksa_hash = hashlib.sha256(ksa_seed).digest()
ksa = generate_ksa(ksa_hash, 256)
payload_swaps = []

for b in transform_output:
    idx = b & 0xff
    payload_swaps.append(ksa[idx] & 0xff)

# Step 4 Block Shuffle
permutation_count = len(payload_swaps) // 16
block_shuffle_seed = xor_seed_key + random_iv
block_shuffle_hash = hashlib.sha256(block_shuffle_seed).digest()
perm_ksa = generate_ksa(block_shuffle_hash, permutation_count)
shuffled = shuffle_blocks(payload_swaps, perm_ksa)

# Setp 5 Final Permutation
length_byte = bytes([len(shuffled)])
perm_seed = aes_key + random_iv + length_byte
perm_hash = hashlib.sha256(perm_seed).digest()
perm_s_box = generate_ksa(perm_hash, 112)

final_payload = []
for i in range(len(perm_s_box)):
    final_payload.append(shuffled[perm_s_box[i]])

swap_order = []
for v in perm_ksa:
        swap_order.extend([v, 0, 0, 0])

final_buffer = bytes(swap_order) + bytes(final_payload)

# Hash Footer
footer_hash = hashlib.sha256(final_buffer).digest()
footer = footer_hash[:8]
version_buf = bytes([1])
perm_length_buf = bytes([permutation_count, 0])
final_packet = (version_buf + random_iv + perm_length_buf + final_buffer + footer)

# Encode final packet
encoded = custom_encode(final_packet)
reversed_bytes = encoded.encode()[::-1]
servers_token = reversed_bytes.hex()

# Get streaming servers
static_path = "hezushon/8ee77bc2e110fd6e6ac7659b33c6f9146497cb81b1a2694590a68f22c5b495b9/APA91DQqR0e_8UTJpaNhNS9c2Bgrg21PeT12bVxpsCvoUhB9rNLJgMZMHxO7oigbPWv7eXn4NavycM9jt2EGVHBmkXIeSJUXh2AOEvWyji1iNx4Txr2OZONKK5IjKp8GBmmzCCb6-rh1I0o50c5eLc_cZ6KnwX7TrB_UsqfYsbMwBqhvWBEEZ1Q/bdf45bbf7c054d8a75d7575767e40745f967d0a8"
api_servers = f"https://vidfast.pro/{static_path}/N1dm4OEpPc8/{servers_token}"
response = requests.get(api_servers, headers=headers).json()

# Select a random server
server = response[0]['data']
api_stream = f"https://vidfast.pro/{static_path}/HSgMMZOauoo/{server}"
response = requests.get(api_stream, headers=headers).json()

# Extract video URL
video_url = response['url']

# Print results
print("\n" + "#" * 25 + "\n" + "#" * 25)
print(f"Captured URL: {Colors.okgreen}{video_url}{Colors.endc}")
print("#" * 25 + "\n" + "#" * 25)
print(f"{Colors.warning}### Use these headers to access the URL")
print(f"{Colors.okcyan}Referer:{Colors.endc} {default_domain}")
print("\n")
