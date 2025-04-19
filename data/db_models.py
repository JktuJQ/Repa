# Imports
from data.db_sesions import databases


# db.sqlite
Note = None
NoteType = None


def load_models():
    """Loads all models from databases"""

    global Note, NoteType

    db_database = databases["db"].classes

    Note = db_database.notes
    NoteType = db_database.notes_type
