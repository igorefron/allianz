# python run.py --api_key=1234
# python run.py --debug

import argparse
import os
from app import create_app

# Create an argument parser
parser = argparse.ArgumentParser(description='Run the Flask application')
parser.add_argument('--api_key', type=str, default=None, help='API Key')
parser.add_argument('--debug', action='store_true', help='Run in debug mode')

# Parse the command-line arguments
args = parser.parse_args()

app = create_app()

# Save the API key for later use
os.environ['API_KEY'] = args.api_key

if __name__ == "__main__":    
    app.run(host='0.0.0.0', port=5000, debug=args.debug)   
