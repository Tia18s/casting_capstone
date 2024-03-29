from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from app.database_helper import BindDBToApp, EnableDBMigrations
from app.models import Movie, Actor
from app.controllers import setupControllers
from app.auth import *
from app.authControllers import setupAuthController
from dotenv import find_dotenv, load_dotenv
from flask_cors import CORS

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

'''Initialize Flask application'''
app = Flask(__name__)

'''Load configuration settings from the Config class'''
app.config.from_object(Config)

'''Bind SQLAlchemy database to the Flask application'''
db = BindDBToApp(app)

'''Enable database migrations for the Flask application'''
migrate = EnableDBMigrations(app, db)

'''Enable CORS for the Flask application'''
CORS(app)

'''Setup authentication controllers for the Flask application'''
setupAuthController(app)

'''Setup controllers for handling application routes and endpoints'''
setupControllers(app)
