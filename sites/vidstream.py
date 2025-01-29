import requests
import re
import base64
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Util.Padding import unpad, pad
import struct

## Library v4.5 ##

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


# Convert byte array to 32-bit word array
def bytes_to_32bit_words(byte_data):
    """
    Converts a byte array into a 32-bit word array.
    """
    words = []
    for i in range(0, len(byte_data), 4):
        word = 0
        for j in range(4):
            if i + j < len(byte_data):
                word |= byte_data[i + j] << (24 - j * 8)
        words.append(struct.unpack('>i', struct.pack('>I', word))[0])
    return words


base_url = "https://vidstreamnew.xyz/v/EDMfWZnXmaYU/"
user_agent = "Mozilla/5.0 (Linux; Android 11; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"
headers = {
    'Referer': "https://vidstreamnew.xyz/",
    'User-Agent': user_agent
}

# Fetch the initial response
initial_response = requests.get(base_url, headers=headers).text

# Extract encrypted data using regex
encrypted_data_match = re.search(r"const\s+Matrix\s*=\s*'(.*?)'", initial_response)
if not encrypted_data_match:
    print("No encrypted data found.")
    exit()

encrypted_data = encrypted_data_match.group(1)

# Decryption process
password = "0-4_xSb3ikmo]&v%D,&7"

# Decode the encrypted data
decoded_bytes = base64.b64decode(encrypted_data)

# Convert bytes to 32-bit word array
result_words = bytes_to_32bit_words(decoded_bytes)

# Extract the IV (initialization vector)
iv = result_words[:4]
iv_bytes = b''.join(word.to_bytes(4, byteorder='big', signed=True) for word in iv)

# Generate a dynamic password with password and User-Agent
dynamic_password = f"{password}{user_agent}"

# Generate the key using SHA256 hash of the password
key = SHA256.new(dynamic_password.encode()).digest()

# Initialize the AES cipher in CBC mode
cipher = AES.new(key, AES.MODE_CBC, iv_bytes)

# Extract the ciphertext
cipher_text = b''.join(
    word.to_bytes(4, byteorder='big', signed=True) for word in result_words[4:]
)

# Decrypt and unpad the plaintext
decrypted_data = unpad(cipher.decrypt(cipher_text), AES.block_size).decode('utf-8')

#Get the video file URL
video_url_pattern = r'file:\s*"([^"]+)"'
video_url_match = re.search(video_url_pattern, decrypted_data)

video_url = ""
if video_url_match:
    video_url = video_url_match.group(1)
else:
    print("No video URL found.")

# Print Results
print("\n" + "#"*25 + "\n" + "#"*25)
print(f"Captured URL: {Colors.okgreen}{video_url}{Colors.endc}")
print("#"*25 + "\n" + "#"*25)
print(f"{Colors.warning}### Please use the header \"Referer: https://vidstreamnew.xyz\" or the CDN host to access the URL, along with the User-Agent: {Colors.okcyan}[{user_agent}]{Colors.endc}\n")
