# Imports
from data.db_sesions import full_init, dbs
from data.db_models import load_models

full_init(dbs)
load_models()


# noinspection PyUnresolvedReferences
def main():
    """ Program's entry point."""
    from backend.application import run

    from backend.routes.page_routes import index, dashboard
    from backend.routes.auth_routes import login, logout, registration

    run()


if __name__ == '__main__':
    main()
