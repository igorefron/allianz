import requests

def fetch_comments(subfeddit, limit=25):
    url = f"https://feddit.api/{subfeddit}/comments?limit={limit}"
    response = requests.get(url)
    return response.json()
