from extensions import db
from datetime import datetime

# Table Avis
class Avis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    commentaire = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(50), nullable=False, default='en attente')  # Exemple: en attente, validé, refusé

    # Lien avec la commande
    commande_id = db.Column(db.Integer, db.ForeignKey('commande.id'))
    commande = db.relationship('Commande', back_populates='avis')

    # Client qui a créé l'avis
    client_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    client = db.relationship('User', foreign_keys=[client_id], back_populates='avis_clients')

    # Admin qui a modéré l'avis
    admin_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    admin = db.relationship('User', foreign_keys=[admin_id], back_populates='avis_admins')
