# helper.py
import requests
import json
import time
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import sys
import random

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

with open('config.json', 'r') as file:
    config = json.load(file)

def get_main_domain():
    return config.get('main_domain')

def get_cookie():
    updated_at = config.get('updated_at')
    cookie = config.get('cookie')

    if cookie and updated_at:
        updated_time = datetime.fromisoformat(updated_at)
        now = datetime.now()

        # Check if less than 24 hours old
        if now - updated_time < timedelta(hours=24):
            return cookie

    # If cookie is missing or expired
    return get_new_cookie()

# Get new cookie if expired
def get_new_cookie():
    print(f'{Colors.okcyan}Getting new cookie please wait 20s(min)...!!{Colors.endc}')
    main_domain = config.get('main_domain')
    verify_domain = config.get('verify_domain')
    
    # Get hash
    response = requests.get(f'{main_domain}/mobile/home')
    if response.status_code == 200:
        response = response.text
    else:
        sys.exit(f"{Colors.fail}Failed to get initial page!{Colors.endc}")

    # Get Add Hash
    soup = BeautifulSoup(response, 'html.parser')
    add_hash = soup.select_one('body')['data-addhash']
    
    # Start verification proccess
    verification_url = f'{verify_domain}?fr3={add_hash}&a=y&t={random.random()}'
    requests.get(verification_url)
    
    # Get Cookie
    new_cookie = None
    while True:
        time.sleep(1)
        data = {"verify": add_hash}
        response = requests.post(f"{main_domain}mobile/verify2.php", data=data)
        res_text = response.text
        if "All Done" in res_text:
            new_cookie = response.cookies.get('t_hash_t')
            break
    
    if not new_cookie:
        sys.exit(f"{Colors.fail}Failed to get new cookie.{Colors.endc}")
    # Save the cookie and return
    save_cookie(new_cookie)
    return new_cookie

def save_cookie(cookie_value, filename="config.json"):
    with open(filename, "r") as file:
        config = json.load(file)

    # Update cookie and timestamp
    config["cookie"] = cookie_value
    config["updated_at"] = datetime.now().isoformat()

    # Save back to file
    with open(filename, "w") as file:
        json.dump(config, file, indent=4)

    print(f"{Colors.okgreen}Cookie saved successfully!!{Colors.endc}")