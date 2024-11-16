from flask import Flask
from flask_pymongo import PyMongo
from routes.parking_routes import parking_bp
from config import Config
import os

app = Flask(__name__)
app.config.from_object(Config)

mongo = PyMongo(app)

# Registrar las rutas del blueprint
app.register_blueprint(parking_bp, url_prefix='/api/parking')

@app.route('/')
def index():
    return "Welcome to PARK AI API"

if __name__ == '__main__':
    app.run(debug=True)
