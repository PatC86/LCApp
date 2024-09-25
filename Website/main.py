# Name: Main
# Author: Patrick Cronin
# Date: 02/08/2024
# Updated: 24/09/2024
# Purpose: Main Python file to Run 'LiftingChainWebApp' From.

from Website import create_App
import logging
from logging.handlers import RotatingFileHandler

# Initialise the flask application
App = create_App()

# Exception handling for app start up
if __name__ == '__main__':
    try:
        handler = RotatingFileHandler('error.log', maxBytes=10000, backupCount=1)
        handler.setLevel(logging.ERROR)
        App.logger.addHandler(handler)
        App.run(debug=True)
    except Exception as e:
        App.logger.error(f"Error occurred during application start up: {e}")
        print(f"Error: {e}")
