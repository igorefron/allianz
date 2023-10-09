from typing import List, Dict, Optional
import requests
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO)

# Constants
BASE_URL = "https://oauth.reddit.com"

def fetch_comments(subreddit: str, limit: int = 25, access_token: Optional[str] = None) -> List[Dict[str, str]]:
    try:
        comments_url = f"{BASE_URL}/r/{subreddit}/comments/.json?limit={limit}"

        headers = {
            'User-Agent': 'allianz_app',
            'Authorization': f"bearer {access_token}"
        }

        response = requests.get(comments_url, headers=headers)
        
        if response.status_code != 200:
            logging.error(f"Failed to fetch comments. Status code: {response.status_code}")
            return []

        comments_data = response.json().get('data', {}).get('children', [])
        comments = [{"id": c['data']['id'], "text": c['data']['body']} for c in comments_data]

        return comments
    except Exception as e:
        logging.error(f"An error occurred while fetching comments: {str(e)}")
        return []
