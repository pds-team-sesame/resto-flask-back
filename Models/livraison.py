from extensions import db
from .commande import Commande
from .user import User  

class Livraison(db.Model):
    __tablename__ = 'livraisons'
    
    idlivraison = db.Column(db.Integer, primary_key=True)
    delivery_address = db.Column(db.String(255), nullable=False)
    delivery_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(50), nullable=False)  # Exemple: "En cours", "Livré", "Annulé", etc.
    #commande_id = db.Column(db.Integer, db.ForeignKey('commandes.id'), nullable=False)
    #livreur_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Référence à user eli howa livreur
    
    # relation m3a table commande
    #commande = db.relationship('Commande', backref='livraison', lazy=True)
    
    # relation bin user w table livraison en tant que livreur
    #livreur = db.relationship('User', backref='livraisons', lazy=True)  

    def __init__(self, delivery_address, delivery_date, status, commande_id, livreur_id):
        self.delivery_address = delivery_address
        self.delivery_date = delivery_date
        self.status = status
        #self.commande_id = commande_id
        #self.livreur_id = livreur_id

    @property
    def data(self):
        return {
            'idlivraison': self.idlivraison,
            'delivery_address': self.delivery_address,
            'delivery_date': self.delivery_date,
            'status': self.status,
            #'commande_id': self.commande_id,
            #'livreur_id': self.livreur_id
        }

    def __repr__(self):
        return f'<Livraison {self.idlivraison} - {self.status} - Livre par {self.livreur_id}>'
    def save(self):
        db.session.add(self)  
        db.session.commit() 