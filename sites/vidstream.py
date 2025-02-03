import requests
import re

## Library v7.1 ##

'''
Supports:
https://vidstreamnew.xyz/
https://moviesapi.club/
https://chillx.top/
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


# Function to perform XOR operation
# The index increments in steps of 3
def decrypt_xor(encrypted_data, password):
    return bytearray(
        [int(encrypted_data[i:i+3]) ^ ord(password[i//3 % len(password)]) 
         for i in range(0, len(encrypted_data), 3)]
    ).decode('utf-8', errors='ignore')

# Initializing static variables
base_url = "https://vidstreamnew.xyz/v/EDMfWZnXmaYU/"
user_agent = "Mozilla/5.0 (Linux; Android 11; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"
headers = {
    'Referer': "https://vidstreamnew.xyz/",
    'User-Agent': user_agent
}

# Fetch the initial response
initial_response = requests.get(base_url, headers=headers).text

# Extract encrypted data using regex
encrypted_data_match = re.search(r"const\s+\w+\s*=\s*'(.*?)'", initial_response)
if not encrypted_data_match:
    print("No encrypted data found.")
    exit()

#Get Encrypted Data and Initialize password
encrypted_data = encrypted_data_match.group(1)
password = "TGRKeQCC8yrxC;5)"

# Obtain the result by applying the XOR operation
decrypted_data = None
if encrypted_data_match:
    encrypted_data = encrypted_data_match.group(1)
    decrypted_data = decrypt_xor(encrypted_data, password)
else:
    print("No encrypted data found.")

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
print(f"{Colors.warning}### Please use the header \"Referer: https://vidstreamnew.xyz\" or the CDN host to access the URL, along with a User-Agent: {Colors.okcyan}[{user_agent}]{Colors.endc}\n")
