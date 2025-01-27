from extensions import db
from datetime import datetime

class Avis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    commentaire = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(50), nullable=False, default='en attente')
    commande_id = db.Column(db.Integer, db.ForeignKey('commande.id'))
    commande = db.relationship('Commande', back_populates='avis')
    client_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    client = db.relationship('User', foreign_keys=[client_id], back_populates='avis_clients')
    admin_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    admin = db.relationship('User', foreign_keys=[admin_id], back_populates='avis_admins')

    def to_dict(self):
        return {
            "id": self.id,
            "commentaire": self.commentaire,
            "rating": self.rating,
            "date": self.date.strftime("%Y-%m-%d %H:%M:%S"),
            "status": self.status,
            "commande_id": self.commande_id,
            "client_id": self.client_id,
            "admin_id": self.admin_id,
        }
