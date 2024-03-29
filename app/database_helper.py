# This file maintains the DB configuration including
# DB app binding and Migration setup

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Initialize SQLAlchemy object
db = SQLAlchemy()

# Function to bind the database to the Flask application


def BindDBToApp(app):
    """
    Bind SQLAlchemy database to the Flask application.

    Args:
        app (Flask): The Flask application instance.

    Returns:
        SQLAlchemy: The SQLAlchemy database object.
    """
    # Load configuration settings from the 'config' module
    app.config.from_object('config')
    # Bind the SQLAlchemy database to the Flask application
    db.app = app
    db.init_app(app)
    return db

# Function to enable database migrations for the Flask application


def EnableDBMigrations(app, db):
    """
    Enable database migrations for the Flask application.

    Args:
        app (Flask): The Flask application instance.
        db (SQLAlchemy): The SQLAlchemy database object.

    Returns:
        Migrate: The database migration object.
    """
    return Migrate(app, db)

# Function to get the application-bound database context


def GetAppBoundDBContext():
    """
    Get the application-bound database context.

    Returns:
        SQLAlchemy: The SQLAlchemy database object bound to the Flask application.
    """
    return db
