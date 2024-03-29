import os
from src import create_app

if __name__ == '__main__':
    debug = os.environ.get('FLASK_DEBUG', 0)
    application = create_app()
    # Dockerfile need host = '0.0.0.0' thats enable to connect every IP
    application.run(debug = debug, host='0.0.0.0')