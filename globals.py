# Imports
import dotenv

from enum import Enum


# Secrets
SECRETS = dotenv.dotenv_values()

FLASK_SECRET_KEY: str = SECRETS["FLASK_SECRET_KEY"]

# Folders
TEMPLATE_FOLDER: str = "../frontend/templates"
STATIC_FOLDER: str = "../frontend/static"


# Website-related
DEBUG = True

FILE_TYPES: set[str] = {"notes", "cheatsheets", "textbooks", "videos", "clips"}
