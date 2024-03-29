import os


class Config:
    """
    Configuration class for Flask application.

    Attributes:
        SQLALCHEMY_DATABASE_URI (str): Database URI. Uses environment variable if available, otherwise defaults to a local PostgreSQL URI.
        SQLALCHEMY_TRACK_MODIFICATIONS (bool): Flag to track modifications. Set to False to suppress modification tracking for SQLAlchemy.
    """

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URI') or 'postgresql://postgres:pg123@localhost:5432/casting_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
