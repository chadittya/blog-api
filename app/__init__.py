from flask import Flask
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager
from flask_swagger_ui import get_swaggerui_blueprint
import os
from urllib.parse import quote_plus

app = Flask(__name__, static_folder='../static')

# Configure MongoDB
mongo_uri = f"mongodb+srv://{os.environ.get('MONGO_USERNAME')}:{os.environ.get('MONGO_PASSWORD')}@{os.environ.get('MONGO_HOST')}/{os.environ.get('MONGO_DB')}?retryWrites=true&w=majority"
app.config["MONGO_URI"] = mongo_uri
mongo = PyMongo(app)

# Configure JWT
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")
jwt = JWTManager(app)

# Configure Swagger UI
SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
API_URL = '/static/swagger.json'  # Our API url (can of course be a local resource)

# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Blog API"
    },
)

# Register blueprint at URL
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# Import routes at the end to avoid circular imports
from app import routes
