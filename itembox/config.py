import os
import connexion
from dotenv import load_dotenv
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# Load .env
load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

# Create the connexion application instance
connex_app = connexion.App(__name__, specification_dir=basedir)

# Get the underlying Flask app instance
app = connex_app.app

# Configure the SqlAlchemy part of the app instance
app.config["SQLALCHEMY_ECHO"] = True if os.getenv("SQLALCHEMY_ECHO") == "true" else False
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True if os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS") == "true" else False

# Create the SqlAlchemy db instance
db = SQLAlchemy(app)

# Initialize Marshmallow
ma = Marshmallow(app)

# Create db migration
migrate = Migrate()

# CORS
CORS(app)