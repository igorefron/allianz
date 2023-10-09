from flask import Blueprint, request, jsonify, render_template, session, Response
from typing import Generator, Any
from .utils.fetch_comments import fetch_comments
from .utils.analyze_sentiment import analyze_sentiment
from .utils.get_access_token import get_access_token
import logging
import json
import pandas as pd

bp = Blueprint('routes', __name__)

# Initialize logging
logging.basicConfig(level=logging.INFO)

@bp.route('/')
def index() -> str:
    return render_template('index.html')

def refresh_token() -> None:
    access_token, expires_in = get_access_token()
    session['access_token'] = access_token    
    session['expires_in'] = expires_in + pd.Timestamp.now().timestamp()

def generate_stream(comments: list) -> Generator[str, None, None]:
    for comment in comments:
        polarity, classification, explanation = analyze_sentiment(comment['text'])
        comment.update({
            'polarity': polarity,
            'classification': classification,
            'explanation': explanation
        })
        yield f"data: {json.dumps(comment)}\n\n"

@bp.route('/analyze_comments', methods=['GET'])
def analyze_comments() -> Any:
    try:
        subreddit = request.args.get('subreddit')
        access_token = session.get('access_token')
        expires_in = session.get('expires_in')
        
        if not access_token or (expires_in and pd.Timestamp.now().timestamp() > expires_in):
            refresh_token()

        comments = fetch_comments(subreddit, access_token=session['access_token'])
        return Response(generate_stream(comments), content_type='text/event-stream')

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return jsonify({"error": str(e)}), 500
