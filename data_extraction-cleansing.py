import requests
# API endpoint
endpoint = 'https://api.sec-api.io/extractor'

# parameters
url = 'https://www.sec.gov/ix?doc=/Archives/edgar/data/789019/000095017023035122/msft-20230630.htm'
item = '7'
token = '2b14839b47fcd6dd9e915831a791a681e2e2fb1ed5e0e600461194d33c6b571c'
item_type = 'html'

# Construct parameters
params = {
    'url': url,
    'item': item,
    'type': item_type,
    'token': token
}

try:
    # Make GET request to the API
    response = requests.get(endpoint, params=params)
    response.raise_for_status()  # Raise exception for HTTP errors

    # Save extracted content to an HTML file
    with open('app8.html', 'w', encoding='utf-8') as f:
        f.write(response.text)
    print("Extracted content saved as 'app8.html'")

    
    

except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
