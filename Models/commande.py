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

    def to_dict(self):
        return {
            "id": self.id,
            "date": self.date.isoformat(),
            "client_id": self.client_id,
            "restaurant_id": self.restaurant_id,
            "livraison": self.livraison.to_dict() if self.livraison else None,
            "paiement": self.paiement.to_dict() if self.paiement else None,
            "avis": self.avis.to_dict() if self.avis else None
        }
