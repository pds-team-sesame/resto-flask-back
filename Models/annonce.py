from extensions import db
from .menu import Menu
from .commande import Commande
from .reservation import Reservation

class Annonce(db.Model):
    __tablename__ = 'annonces'
    
    ida = db.Column(db.Integer, primary_key=True)
    restaurant_name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)
    
    #menu_plats = db.relationship('Menu', backref='annonce', lazy=True)
    #commandes = db.relationship('Commande', backref='annonce', lazy=True)  # Relier commandes à l'annonce
    #reservations = db.relationship('Reservation', backref='annonce', lazy=True)  # Relier réservations à l'annonce
    #user = db.relationship('User', backref=db.backref('annonces', lazy=True))  # Un utilisateur peut gérer plusieurs annonces
    
    def __init__(self, restaurant_name, address, phone_number, description):
        self.restaurant_name = restaurant_name
        self.address = address
        self.phone_number = phone_number
        self.description = description

    @property
    def data(self):
        return {
            'ida': self.ida,
            'restaurant_name': self.restaurant_name,
            'address': self.address,
            'phone_number': self.phone_number,
            'description': self.description,
        }

    def __repr__(self):
        return f'<Annonce {self.restaurant_name}>'
    
    def save(self):
        db.session.add(self)  
        db.session.commit() 