# Imports
from data.db_sesions import full_init, dbs
from data.db_models import load_models

full_init(dbs)
load_models()


# noinspection PyUnresolvedReferences
def main():
    """ Program's entry point."""
    from backend.application import run

    from backend.routes.page_routes import index, dashboard, unified_catalog, catalog, file_download, file_detail
    from backend.routes.auth_routes import login, logout, registration
    from backend.routes.algorithm_routes import upgrade_image

    run()


if __name__ == '__main__':
    main()
