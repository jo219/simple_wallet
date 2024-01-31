from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# app.register_blueprint(api_v1_bp)
from app.routes import (
    ping_routes, 
    user_routes, 
    wallet_read_routes, 
    wallet_write_routes,     
)
