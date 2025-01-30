import requests
import re

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

base_url = "https://mixdrop.ps/e/q1m9d9eeuz13dx"
user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"

headers = {
    'Referer': "https://mixdrop.ps/",
    'User-Agent': user_agent
}


# Fetch the initial response
initial_response = requests.get(base_url, headers=headers).text

pattern = r'eval\(function\((.*?)\)\{.*\}\((.*?)\)\)'
packed_data_match = re.search(pattern, initial_response)


# Extract packed data if found
packed_data = ""
if packed_data_match:
    packed_data = packed_data_match.group(2).replace("\"", "").replace(".split('|')", "").replace("\'","").split(',')
else:
    print("Failed to extract packed data.")

# Function to convert numbers to base-32
def convert_base(n):
    return str(n) if n < 10 else chr(n - 10 + ord('a'))

# Extract variables from packed data
p = packed_data[0]
a = int(packed_data[1])
c = int(packed_data[2])
k = packed_data[3].split('|')
e = int(packed_data[4])

# Decrypt the data
d = {}
while c > 0:
    c -= 1
    d[convert_base(c)] = k[c] if k[c] else convert_base(c)

# Replace function to decode the packed data
final_result = re.sub(r'\b\w+\b', lambda match: d.get(match.group(0), match.group(0)), p)

# Regex to find the video URL
regex_match = re.search(r"MDCore\.wurl=([^;]+)", final_result)

# Get video URL
video_url = ""
if regex_match:
    video_url = f"https:{regex_match.group(1)}"
else:
    print(f"{Colors.fail}Video URL not found!{Colors.endc}")

# Print Results
print("\n" + "#"*25 + "\n" + "#"*25)
print(f"Captured URL: {Colors.okgreen}{video_url}{Colors.endc}")
print("#"*25 + "\n" + "#"*25)
print(f"{Colors.warning}### Please use the header \"Referer: https://mixdrop.ps/\" or the CDN host to access the URL, along with a User-Agent.\n")