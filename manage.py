from flask_migrate import Migrate
from app import app, db

# Initialize Flask app and database migration
migrate = Migrate(app, db)
