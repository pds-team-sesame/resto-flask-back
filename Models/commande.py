from extensions import db
from datetime import datetime

# Table Commande
class Commande(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    client_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'))
    client = db.relationship('User', back_populates='commandes')
    restaurant = db.relationship('Restaurant', backref='commandes')
    livraison = db.relationship('Livraison', back_populates='commande', uselist=False, cascade='all, delete-orphan')
    paiement = db.relationship('Paiement', back_populates='commande', uselist=False, cascade='all, delete-orphan')
    avis = db.relationship('Avis', back_populates='commande', uselist=False, cascade='all, delete-orphan')
