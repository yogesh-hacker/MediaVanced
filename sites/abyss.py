import requests
import re
import ast

'''
Supports:
https://abysscdn.com/
https://hydraxcdn.biz/
'''

# This script is currently under development.  
# It requires further optimization and bug fixes to ensure stability.  
# There may be instances where the script does not function as expected.  
# Please wait until the development process is complete for a stable version.  
# If you have suggestions or improvements, your contributions are highly appreciated!

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
        indexes = [CHARSET.index(c) if c in CHARSET else 64 for c in encoded_str[i:i+4]]
        byte1 = (indexes[0] << 2) | (indexes[1] >> 4)
        byte2 = ((indexes[1] & 15) << 4) | (indexes[2] >> 2)
        byte3 = ((indexes[2] & 3) << 6) | indexes[3]

        decoded_bytes.append(byte1)
        if indexes[2] != 64:
            decoded_bytes.append(byte2)
        if indexes[3] != 64:
            decoded_bytes.append(byte3)

    return decoded_bytes.decode("utf-8", errors="ignore")

def convert_index(index, array_length):
    return index + array_length if index < 0 else index

def convert_array(arr, array_length):
    converted_arr = [convert_index(x, array_length) for x in arr]
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
final_string = decode("".join(decoded_values).replace("_", ""))

print("Concatenated String:", final_string)

# The output may not always be accurate.  
# It should return a valid JSON response containing keys like md5, slug, id, domain, etc.