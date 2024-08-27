import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urlparse
import re
import json 
import json
import base64
import codecs

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def save_file_in_internal_directory(filename, content, directory='/storage/emulated/0'):
    file_path = os.path.join(directory, filename)
    try:
        with open(file_path, 'w') as file:
            file.write(content)
        print(f"File saved to {file_path}")
    except Exception as e:
        print(f"Error saving file: {e}")
    

default_domain = "https://www.dailymotion.com/"
initial_headers = {
    'Referer': default_domain,
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36'
}
print(f"\n{Colors.OKCYAN}TARGET: {default_domain}{Colors.ENDC}")

cookies = {
    'ui': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE3MjAzNTgxMjQsIm5iZiI6MTcyMDM1ODEyNCwiZXhwIjoxNzUxNDYyMTQ0LCJkYXRhIjp7InVpZCI6NDU0MDA0LCJ0b2tlbiI6IjdjNmMwMzEzYThhOGUzOTczNGZjMDI2MDQ2Y2JlNzkzIn19.LXWUfS004XLU6irNvIiNbxmG0weQ-mjZr7rzUhQdBjk'
}

proxy = {
    "http": "http://qvgxntjn:1cyxq9jfd6rh@45.127.248.127:5128",
    "https": "http://qvgxntjn:1cyxq9jfd6rh@45.127.248.127:5128"
}

base_url = "https://www.dailymotion.com/player/metadata/video/x8qqe3e"
session = requests.Session()

initial_response = session.get(base_url, headers=initial_headers)
json_content = initial_response.json()

playlist_url = json_content["qualities"]["auto"][0]["url"]
initial_response = requests.get(playlist_url, headers=initial_headers)

playlist_content = initial_response.text
pattern = re.compile(r'NAME="(\d+)".*?PROGRESSIVE-URI="(.*?)".*?\s(https://\S+)')

matches = pattern.findall(playlist_content)

for match in matches:
    resolution = match[0]
    progressive_url = match[1]
    live_streaming_url = match[2]
    print(f'{Colors.OKGREEN}Resolution:{Colors.ENDC} {resolution}p')
    print(f'{Colors.OKGREEN}Progressive URL: {Colors.ENDC}{progressive_url}')
    print(f'{Colors.OKGREEN}Streaming URL: {Colors.ENDC}{live_streaming_url}')
    print('---------')
    print('---------')