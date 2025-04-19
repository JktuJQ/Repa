# Imports
import os

from flask import Flask


TEMPLATE_FOLDER = "../frontend/templates"
STATIC_FOLDER = "../frontend/static"

application = Flask(__name__, template_folder=TEMPLATE_FOLDER, static_folder=STATIC_FOLDER)
application.config["SECRET_KEY"] = os.getenv("SECRET_KEY")


def run(port: int = 8080, host: str = "127.0.0.1"):
    """Runs application on 'http://{host}:{port}/'"""
    application.run(port=port, host=host)
