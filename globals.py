# Imports
import os

import dotenv

from enum import Enum


# Secrets
SECRETS = dotenv.dotenv_values()

FLASK_SECRET_KEY: str = SECRETS["FLASK_SECRET_KEY"]
YANDEX_SECRET_KEY: str = SECRETS["YANDEX_SECRET_KEY"]

# Folders
TEMPLATE_FOLDER: str = "../frontend/templates"
STATIC_FOLDER: str = "../frontend/static"

UPLOAD_FOLDER: str = "../data/files"
LECTURES_FOLDER: str = os.path.join(UPLOAD_FOLDER, "notes")
SEMINARS_FOLDER: str = os.path.join(UPLOAD_FOLDER, "cheatsheets")

# Website-related
DEBUG = True

MAX_FILE_SIZE: int = 100 * 1024 * 1024


def file_extension(filename: str) -> str:
    """Returns file extension of given file."""
    if "." in filename:
        return filename.rsplit(".", 1)[1].lower()
    return ""


class NotesFileType(Enum):
    """Enumeration that represents type of notes."""

    IMAGE = 1
    VIDEO = 2

    @property
    def extensions(self) -> set[str]:
        """Returns set of allowed extensions for this note type"""
        if self == self.IMAGE:
            return {"png", "jpg", "jpeg", "pdf"}
        elif self == self.VIDEO:
            return {"mp4", "mov", "avi"}

    def is_allowed_file(self, filename: str) -> bool:
        """Checks whether filename is allowed for this type."""
        return file_extension(filename) in self.extensions
