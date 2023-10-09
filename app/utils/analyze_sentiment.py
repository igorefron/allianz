import openai
import json
import os
from textblob import TextBlob

def analyze_sentiment(comment):
    try:
        openai.api_key = os.environ.get('API_KEY') 
        prompt_text = f'''make a sentiment analysis on following comment:
        "{comment}"

        Return results as json, with following attributes
        "polarity_score",
        "sentiment",
        "explanation"
        '''
        completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "assistant", "content": prompt_text}])
        content = completion.choices[0].message.content
        # Parse content to extract polarity_score, sentiment, and explanation
        # Assuming the content is a JSON string
        result = json.loads(content)
        return result['polarity_score'], result['sentiment'].lower(), result['explanation']
    except Exception as e:
        # Fallback to TextBlob
        analysis = TextBlob(comment)
        polarity = analysis.sentiment.polarity
        classification = "positive" if polarity > 0 else "negative"
        explanation = ""  # Initialize an empty string for explanation
        return polarity, classification, explanation