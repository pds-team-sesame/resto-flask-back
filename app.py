from flask import Flask
from config import Config
from extensions import db
from flask_migrate import Migrate
from Models.user import User
from Models.commande import Commande
from Models.reservation import Reservation
from Models.avis import Avis
from Models.livraison import Livraison
from Models.menu import Menu
from Models.paiement import Paiement
from Models.restaurant import Restaurant
from Models.role import Role
from Models.table import Table
from routes import main
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:4200"}})
    app.config.from_object(Config)
    register_resources(app)
    migrate = register_extensions(app)
    return app

def register_extensions(app):
    db.init_app(app)
    migrate = Migrate(app, db)
    return migrate

def register_resources(app):
    app.register_blueprint(main)


if __name__ == '__main__':
    app = create_app()
    app.run('127.0.0.1', 5000)
