from extensions import db
from .roles import Role
from .commande import Commande
from .reservation import Reservation
from .avis import Avis

class User(db.Model):
    __tablename__ = 'users'  

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(80), nullable=False)
    prenom = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.idrole'))  # Correction de la relation avec 'roles'
    role = db.relationship('Role', backref=db.backref('users', uselist=True))  # Correct backref
    commandes = db.relationship('Commande', backref='user', lazy=True)
    reservations = db.relationship('Reservation', backref='user', lazy=True)
    avis = db.relationship('Avis', backref='user', lazy=True)

    def __init__(self,  email, role_id,nom,prenom,password):
        self.email = email
        self.role_id = role_id
        self.nom = nom
        self.prenom = prenom
        self.password = password


    @property
    def data(self):
        return {
            'id': self.id,
            'email': self.email,
            'role': self.role.data,
            'nom' : self.nom ,
            'prenom':  self.prenom ,
            'password'   :self.password ,
            'commandes': [commande.data for commande in self.commandes],
            'reservations': [reservation.data for reservation in self.reservations],
            'avis': [avis.data for avis in self.avis]
        }

    def save(self):
        db.session.add(self)  
        db.session.commit() 