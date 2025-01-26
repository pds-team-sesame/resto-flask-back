from extensions import db
from sqlalchemy import Enum
from Models.role import Role

# Table User
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), unique=True, nullable=False)
    role = db.Column(Enum(Role), nullable=False)

    # Relations
    restaurants = db.relationship('Restaurant', back_populates='gerent', cascade='all, delete-orphan')  # Gérant
    commandes = db.relationship('Commande', back_populates='client', cascade='all, delete-orphan')  # Client
    livraisons = db.relationship('Livraison', back_populates='livreur', cascade='all, delete-orphan')  # Livreur
    reservations = db.relationship('Reservation', back_populates='client', cascade='all, delete-orphan')  # Client
    avis_clients = db.relationship('Avis', foreign_keys='Avis.client_id', back_populates='client')  # Avis laissés par le client
    avis_admins = db.relationship('Avis', foreign_keys='Avis.admin_id', back_populates='admin')  # Avis modérés par l'admin

    # Ajouter la méthode to_dict à l'intérieur de la classe User
    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "password":self.password,
            "role": self.role.value  # Affiche la valeur du rôle (par exemple "admin")
        }
