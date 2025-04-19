# Imports
import sys
import typing as t

from data.db_sesions import full_init, dbs
from data.models import load_models

full_init(dbs)
load_models()


def main(argv: t.List[str]):
    """ Program's entry point."""
    from backend.application import run
    from backend.routes import index
    run()


if __name__ == '__main__':
    main(sys.argv)
