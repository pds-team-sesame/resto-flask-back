# facturation.py
from extensions import db

class Facturation(db.Model):
    __tablename__ = 'facturations'
    
    idfact = db.Column(db.Integer, primary_key=True)
    total_amount = db.Column(db.Float, nullable=False)
    #commande_id = db.Column(db.Integer, db.ForeignKey('commandes.idc'), nullable=False)
    
    #commande = db.relationship('Commande', backref='facturation', lazy=True)
    
    def __init__(self, total_amount ): #,commande_id
        self.total_amount = total_amount
       # self.commande_id = commande_id

    @property
    def data(self):
        return {
            'idfact': self.idfact,
            'total_amount': self.total_amount,
            #'commande_id': self.commande_id
        }

    def __repr__(self):
        return f'<Facturation {self.idfact} - {self.total_amount}>'
    
    def save(self):
        #from .commande import Commande  # Importation locale pour éviter la circularité
        db.session.add(self)
        db.session.commit()
