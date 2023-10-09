from typing import Tuple, Optional
import requests
from requests.auth import HTTPBasicAuth
import logging
import os

# Initialize logging
logging.basicConfig(level=logging.INFO)

# Constants
TOKEN_URL = "https://www.reddit.com/api/v1/access_token"

# Load sensitive information from environment variables
CLIENT_ID = "mC4mwlVRXLQCI6Jn982LFA"
CLIENT_SECRET = os.environ.get('API_SECRET')

def get_access_token() -> Tuple[Optional[str], Optional[int]]:
    try:
        auth = HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
        data = {
            'grant_type': 'client_credentials'
        }
        headers = {'User-Agent': 'allianz-app'}
        
        res = requests.post(TOKEN_URL, auth=auth, data=data, headers=headers)
        
        if res.status_code != 200:
            logging.error(f"Failed to get access token. Status code: {res.status_code}")
            return None, None

        return res.json().get('access_token'), res.json().get('expires_in')
    except Exception as e:
        logging.error(f"An error occurred while getting the access token: {str(e)}")
        return None, None