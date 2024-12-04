from extensions import db
from .menu import Menu
from .facturation import Facturation

class Commande(db.Model):
    __tablename__ = 'commandes'
    
    idc = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # Correction de 'user_id'
    user = db.relationship('User', backref='commandes')
    menu_id = db.Column(db.Integer, db.ForeignKey('menus.idm'))  # Correction de la relation avec le menu
    
    # Relations avec Facturation et Paiement
    facturation = db.relationship('Facturation', backref='commande', uselist=False)
    paiement = db.relationship('Paiement', backref='commande', uselist=False)

    def __init__(self, date, user_id):
        self.date = date
        self.user_id = user_id

    @property
    def data(self):
        return {
            'idc': self.idc,
            'date': self.date,
            'user': self.user.data,
            'menus': [menu.data for menu in self.menu]
        }
    def save(self):
        db.session.add(self)  
        db.session.commit() 