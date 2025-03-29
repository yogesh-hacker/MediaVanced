import requests
import re
import base64
import codecs

'''
Supports:
https://swift.multiquality.click/
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
base_url = "https://swift.multiquality.click/embed/P9XAC2GgcqcjdMp"
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
initial_headers = {
    'Referer': 'https://swift.multiquality.click',
    'Connection': 'keep-alive',
    'User-Agent': user_agent
}

# Utility Functions
def decodeSalt(e):
    t = ""
    for c in e:
        t += str(ord(c) - 100)
    return t

session = requests.Session()

# Fetch response
response = session.get(base_url, headers=initial_headers).text

# Extract and evaluate the code
code = re.findall(r'_juicycodes\(([^\)]+)', response, re.IGNORECASE)[0]
code = eval(code)

# Process the salt and the obfuscated JavaScript code
salt = ''.join([str(ord(char) - 100) for char in code[-3:]])
encoded_js = code[:-3]
padding_len = (len(encoded_js) + 3) % 4
encoded_js += "==="[:-padding_len]
encoded_js = encoded_js.replace("_", "+").replace("-", "/")

# Base64 decode and then ROT13 decode the result
decoded_js = codecs.decode(codecs.decode(encoded_js.encode('ascii'), 'base64').decode('ascii'), 'rot13')

# Map symbols to their corresponding index values and process them
symbol_map = ["`", "%", "-", "+", "*", "$", "!", "_", "^", "="]
index_string = ''.join([str(symbol_map.index(char)) for char in decoded_js])

# Split the index_string into chunks of 4 characters each
splitted_index = [index_string[i:i + 4] for i in range(0, len(index_string), 4)]

# Decode each chunk back to characters
final_string = ""
for c in splitted_index:
    decoded_char = int(c) % 1000 - int(salt)
    final_string += chr(decoded_char)

# Finalize by sanatizing the output
decrypted_data = final_string.replace(r'\/', '/')

# Extract video URL
regex = r'"file":"(https:\/\/[^"]+\.m3u8)"'
video_url = re.search(regex, decrypted_data).group(1)

# Print results
print("\n" + "#" * 25 + "\n" + "#" * 25)
print(f"Captured URL: {Colors.okgreen}{video_url}{Colors.endc}")
print("#" * 25 + "\n" + "#" * 25 + "\n")
