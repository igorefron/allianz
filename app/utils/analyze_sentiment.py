from textblob import TextBlob

def analyze_sentiment(comment):
    analysis = TextBlob(comment)
    polarity = analysis.sentiment.polarity
    return polarity, "positive" if polarity > 0 else "negative"
