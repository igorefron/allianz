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
    
    if not access_token:
        access_token = get_access_token()
        session['access_token'] = access_token
    
    comments = fetch_comments(subreddit, access_token=access_token)
    for comment in comments:
        polarity, classification = analyze_sentiment(comment['text'])
        comment['polarity'] = polarity
        comment['classification'] = classification
    
    return jsonify(comments)