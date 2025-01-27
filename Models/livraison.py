from extensions import db
from datetime import datetime

# Table Livraison
class Livraison(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(50), nullable=False)
    commande_id = db.Column(db.Integer, db.ForeignKey('commande.id'))
    livreur_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    commande = db.relationship('Commande', back_populates='livraison')
    livreur = db.relationship('User', back_populates='livraisons')

    def to_dict(self):
        return {
            "id": self.id,
            "date": self.date.isoformat(),
            "status": self.status,
            "commande_id": self.commande_id,
            "livreur_id": self.livreur_id,
        }
