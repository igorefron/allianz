import unittest
from app import create_app  # Replace with how you import your Flask app
import json

class TestRoutes(unittest.TestCase):

    def setUp(self):        
        self.app = create_app()
        self.client = self.app.test_client()

    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Subreddit Sentiment Analysis', response.data)  # Replace with actual text you expect

    def test_analyze_comments(self):
        response = self.client.get('/analyze_comments?subreddit=science')
        self.assertEqual(response.status_code, 200)
        # Add more assertions based on what you expect the output to be

    # Add more test methods as needed

if __name__ == '__main__':
    unittest.main()
