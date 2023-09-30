import json
import unittest
from flask import Flask
from myproject.app import app

class RoutesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.client = self.app.test_client()

    def test_predict_next_placement(self):
        # Use a dictionary to store your input data
        input_data = {"input": [1, 2, 3, 4]}
        
        # Use test client to send a POST request to the route
        response = self.client.post('/predict_next_placement', 
                                    data=json.dumps(input_data),
                                    content_type='application/json')
        
        # Check that the status code of the response is 200 (HTTP OK)
        self.assertEqual(response.status_code, 200)

    def test_predict_container_template(self):
        # Use a dictionary to store your input data
        input_data = {"input": [1, 2, 3, 4]}
        
        # Use test client to send a POST request to the route
        response = self.client.post('/predict_container_template', 
                                    data=json.dumps(input_data),
                                    content_type='application/json')
        
        # Check that the status code of the response is 200 (HTTP OK)
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()
