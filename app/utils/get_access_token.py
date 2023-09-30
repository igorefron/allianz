import requests
from requests.auth import HTTPBasicAuth

def get_access_token():
    token_url = "https://www.reddit.com/api/v1/access_token"
    client_id = "mC4mwlVRXLQCI6Jn982LFA"
    client_secret = "GeL-UnQ0NqRUwhuBtCLDCbA6Lo1NtA"
    auth = HTTPBasicAuth(client_id, client_secret)
    data = {
        'grant_type': 'client_credentials'
    }
    headers = {'User-Agent': 'allianz-app'}
    
    res = requests.post(token_url, auth=auth, data=data, headers=headers)    
    return res.json().get('access_token')