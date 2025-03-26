import requests
import re
import ast
import sys
import json

## VERSION: 1.0 ##

'''
Supports:
https://abysscdn.com/
https://hydraxcdn.biz/
'''

# This script functions as expected but may occasionally fail.
# It successfully runs in about 90% of cases.
# This script retrieves only the necessary data for video playback.  
# It does NOT return the actual video URL. 
# A custom video player setup is required. 
# The URL requires encryption and POST responses for playback.


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
base_url = "https://abysscdn.com/?v=r05GGctsV"
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
CHARSET = "RB0fpH8ZEyVLkv7c2i6MAJ5u3IKFDxlS1NTsnGaqmXYdUrtzjwObCgQP94hoeW+/="
headers = {
    "Referer": "https://abysscdn.com/",
    "User-Agent": user_agent
}

# Utility Functions
def decode(encoded_str):
    decoded_bytes = bytearray()
    
    for i in range(0, len(encoded_str), 4):
        chunk = encoded_str[i:i+4]
        
        # Ensure the chunk has exactly 4 characters, padding with '=' if needed
        chunk = chunk.ljust(4, "=")  

        indexes = [CHARSET.index(c) if c in CHARSET else 64 for c in chunk]

        byte1 = (indexes[0] << 2) | (indexes[1] >> 4)
        
        # Append bytes conditionally to avoid IndexError
        decoded_bytes.append(byte1)
        if len(indexes) > 2 and indexes[2] != 64:
            byte2 = ((indexes[1] & 15) << 4) | (indexes[2] >> 2)
            decoded_bytes.append(byte2)
        if len(indexes) > 3 and indexes[3] != 64:
            byte3 = ((indexes[2] & 3) << 6) | indexes[3]
            decoded_bytes.append(byte3)

    return decoded_bytes.decode("utf-8", errors="ignore")

def wrap_index(input_index, total_length):
    adjusted_index = input_index + total_length if input_index < 0 else input_index
    if adjusted_index > total_length:
        return adjusted_index - total_length
    return adjusted_index

def convert_array(arr, array_length):
    converted_arr = [wrap_index(x, array_length) for x in arr]
    return converted_arr

# Fetch the webpage content
response = requests.get(base_url, headers=headers).text
pattern = r'[a-zA-Z]\(\d+\)(?:\+[a-zA-Z]\(\d+\)|\+\([^)]+\))*'

# Find all function-like patterns and select the longest match
matched_patterns = re.findall(pattern, response)
longest_match = max(matched_patterns, key=len, default="")

# Extract numerical values from the longest match
extracted_numbers = list(map(int, re.findall(r"\d+", longest_match)))

# Extract the subtraction offset from the response
offset_match = re.search(r"-=(\d+)", response)
offset_value = int(offset_match.group(1))

# Adjust numbers using the extracted offset
adjusted_numbers = [num - offset_value for num in extracted_numbers]

# Extract the obfuscated string array enclosed within square brackets
array_pattern = r"\[(.*?)\]"
obfuscated_arrays = re.findall(array_pattern, response, re.DOTALL)

# Identify the longest array and parse it into a Python list
obfuscated_string_list = ast.literal_eval(f"[{max(obfuscated_arrays, key=len)}]")

# Locate the reference index in the obfuscated array
reference_index = obfuscated_string_list.index('lOyPK5iCK0')

# Calculate the shift value based on the first adjusted number
shift_value = adjusted_numbers[0] - reference_index
final_offset = offset_value + shift_value

# Adjust the extracted numbers using the final offset
final_numbers = [num - final_offset for num in extracted_numbers]

# Convert numbers into valid array indices
converted_indices = convert_array(final_numbers, len(obfuscated_string_list))

# Extract corresponding string values from the obfuscated array
decoded_values = [obfuscated_string_list[idx] for idx in converted_indices if 0 <= idx < len(obfuscated_string_list)]

# Concatenate and decode the final extracted string
decoded_data = None
try:
    decoded_data = decode("".join(decoded_values).replace("_", ""))
except Exception as e:
    print(f"\n{Colors.fail}Decoding failed: {e}{Colors.endc}\n{Colors.okgreen}[RETRY+++] By restarting the script...{Colors.endc}\n")
    sys.exit(1)

# Convert output to JSON
json_data = json.loads(decoded_data)

print(f'\n{Colors.okgreen}METADATA:{Colors.endc} {json_data}')
print(f"\nCaptured URL: {Colors.okgreen}https://{json_data['domain']}/{json_data['id']}\n")
print(f"{Colors.warning}### You may need additional set-up to play these video URLs. Thank You!{Colors.endc}\n")