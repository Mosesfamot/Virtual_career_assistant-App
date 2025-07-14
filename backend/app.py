from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from auth import auth
from routes import routes
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Enable CORS for all origins (adjust if needed for security)
CORS(app, supports_credentials=True, origins=["https://virtual-career-assistant-fn47.vercel.app"])

# Configure JWT
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "your-fallback-secret")
jwt = JWTManager(app)

# Register routes
from auth import auth
from routes import routes

# Register Blueprints
app.register_blueprint(auth, url_prefix="/api/auth")
app.register_blueprint(routes, url_prefix="/api")

# Run the app
if __name__ == "__main__":
    app.run(debug=True)