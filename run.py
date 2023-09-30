# python run.py
# python run.py --debug

import argparse
from app import create_app

# Create an argument parser
parser = argparse.ArgumentParser(description='Run the Flask application')
parser.add_argument('--debug', action='store_true', help='Run in debug mode')

# Parse the command-line arguments
args = parser.parse_args()

app = create_app()

if __name__ == "__main__":    
    app.run(host='0.0.0.0', port=5000)   
    
