from extensions import db
from datetime import datetime
class Paiement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(50), nullable=False)
    commande_id = db.Column(db.Integer, db.ForeignKey('commande.id'))
    commande = db.relationship('Commande', back_populates='paiement')

    def to_dict(self):
        return {
            "id": self.id,
            "amount": self.amount,
            "date": self.date.isoformat(),
            "status": self.status,
            "commande_id": self.commande_id
        }
