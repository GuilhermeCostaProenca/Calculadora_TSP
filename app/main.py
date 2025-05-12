import os
from flask import Flask
from app.routes import configure_routes
from dotenv import load_dotenv
load_dotenv()

def create_app():
    # Caminhos absolutos para garantir que o Flask encontre os arquivos
    base_dir = os.path.abspath(os.path.dirname(__file__))
    template_dir = os.path.join(base_dir, "..", "templates")
    static_dir = os.path.join(base_dir, "..", "static")

    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
    configure_routes(app)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
