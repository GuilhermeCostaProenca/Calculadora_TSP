import os
from flask import Flask
from dotenv import load_dotenv
from app.routes import configure_routes

# Carrega as variáveis do .env
load_dotenv()

def create_app():
    app = Flask(__name__)
    configure_routes(app)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
