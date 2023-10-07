from flask import Blueprint, request, jsonify, render_template, session
from flask import Flask, request, jsonify
from .utils.fetch_comments import fetch_comments
from .utils.analyze_sentiment import analyze_sentiment
from .utils.get_access_token import get_access_token


import numpy as np
import pandas as pd

bp = Blueprint('routes', __name__)

@bp.route('/')
def index():
    return render_template('index.html')


@bp.route('/analyze_comments', methods=['GET'])
def analyze_comments():
    subreddit = request.args.get('subreddit')
    access_token = session.get('access_token')
    expires_in = session.get('expires_in')
    
    if not access_token or (expires_in and pd.Timestamp.now().timestamp() > expires_in):
        access_token, expires_in = get_access_token()
        session['access_token'] = access_token    
        session['expires_in'] = expires_in + pd.Timestamp.now().timestamp()

    comments = fetch_comments(subreddit, access_token=access_token)
    for comment in comments:
        polarity, classification, explanation = analyze_sentiment(comment['text'])
        comment['polarity'] = polarity
        comment['classification'] = classification
        comment['explanation'] = explanation
    
    return jsonify(comments)