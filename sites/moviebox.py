import requests
from urllib.parse import urlparse, parse_qs

'''
Supports:
https://moviebox.ph/
https://fmoviesunblocked.net/
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
base_url = 'https://fmoviesunblocked.net/spa/videoPlayPage/movies/the-fantastic-four-first-steps-AQl6LSd1vC5?id=4717678971557691344&type=/movie/detail&lang=en'
user_agent = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36"
default_domain = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(base_url))
headers = {
    'Referer': default_domain,
    'User-Agent': user_agent
}

# Construct API URL
parsed_url = urlparse(base_url)
detail_path = parsed_url.path.split('/')[-1]
queries = parse_qs(parsed_url.query)
subject_id = queries.get('id')[0]
api_url = f'https://fmoviesunblocked.net/wefeed-h5-bff/web/subject/play?subjectId={subject_id}&se=0&ep=0&detail_path={detail_path}'

# Get streaming data
get_headers ={
    'Referer': base_url,
    'Accept': 'application/json',
    'X-Client-Info': '{"timezone":"Asia/Calcutta"}',
    'X-Source': ''
}
response = requests.get(api_url, headers=get_headers).json()

# Extract video URL(Highest Quality)
streams = response.get('data', {}).get('streams', [])
video_url = max(streams, key=lambda s: int(s.get('resolution', 0)), default={}).get('url')

# Print results
print("\n" + "#" * 25 + "\n" + "#" * 25)
print(f"Captured URL: {Colors.okgreen}{video_url}{Colors.endc}")
print("#" * 25 + "\n" + "#" * 25)
print(f"{Colors.warning}### Use these headers to access the URL")

# Print headers by key: value
for key, value in headers.items():
    print(f"{Colors.okcyan}{key}:{Colors.endc} {value}")
print("\n")