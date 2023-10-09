# python run.py --api_key=1234
# python run.py --debug

import argparse
import os
import logging
from typing import Optional
from app import create_app

def setup_logging() -> None:
    logging.basicConfig(level=logging.INFO)
    logging.info("Logging is set up.")

def main(api_key: Optional[str], api_secret: Optional[str], debug: bool) -> None:
    app = create_app()
    
    # Save the API key and secret for later use
    if api_key:
        os.environ['API_KEY'] = api_key
    if api_secret:
        os.environ['API_SECRET'] = api_secret

    app.run(host='0.0.0.0', port=5000, debug=debug)

if __name__ == "__main__":
    # Create an argument parser
    parser = argparse.ArgumentParser(description='Run the Flask application')
    parser.add_argument('--api_key', type=str, default=None, help='ChatGPT API Key')
    parser.add_argument('--api_secret', type=str, default=None, help='Reddit API Secret')
    parser.add_argument('--debug', action='store_true', help='Run in debug mode')

    # Parse the command-line arguments
    args = parser.parse_args()

    # Setup logging
    setup_logging()

    # Validate API key and secret if necessary
    if args.api_key is None or args.api_secret is None:
        logging.error("API key or API secret is missing. Exiting.")
        exit(1)

    main(api_key=args.api_key, api_secret=args.api_secret, debug=args.debug)

