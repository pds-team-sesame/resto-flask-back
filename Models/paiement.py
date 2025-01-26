from extensions import db
from datetime import datetime

# Table Paiement
class Paiement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(50), nullable=False)
    commande_id = db.Column(db.Integer, db.ForeignKey('commande.id'))
    commande = db.relationship('Commande', back_populates='paiement')
