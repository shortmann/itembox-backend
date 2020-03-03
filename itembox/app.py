import connexion

# local modules
import itembox.config as config


# Create the flask api
def create_app(testing=False, cli=False):
    """Application factory, used to create application
    """
    # Create the application instance
    connex_app = config.connex_app

    # Read the swagger.yml file to configure the endpoints
    connex_app.add_api('swagger.yml')

    app = connex_app.app

    # Migrate
    config.db.init_app(app)
    config.migrate.init_app(app, config.db)

    if testing is True:
        app.config["TESTING"] = True

    return app
