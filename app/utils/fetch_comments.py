import requests
from requests.auth import HTTPBasicAuth

def fetch_comments(subreddit, limit=25, access_token=None):
    
    base_url = "https://oauth.reddit.com"
    comments_url = f"{base_url}/r/{subreddit}/comments/.json?limit={limit}"

    headers = {
        'User-Agent': 'allianz_app',
        'Authorization': f"bearer {access_token}"
    }

    response = requests.get(comments_url, headers=headers)      

    comments_data = response.json().get('data', {}).get('children', [])
    comments = [{"id": c['data']['id'], "text": c['data']['body']} for c in comments_data]    

    return comments