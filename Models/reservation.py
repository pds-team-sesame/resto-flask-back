from extensions import db
from .table import Table


class Reservation(db.Model):
    __tablename__ = 'reservation'
    
    idr = db.Column(db.Integer, primary_key=True)
    horaire = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(100), nullable=False)
    nb_personne= db.Column(db.String(100), nullable=False)
    #user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    #user = db.relationship('User', backref='reservations')
    #table_idt = db.Column(db.Integer, db.ForeignKey('table.idt'))
    #table = db.relationship('Table', backref=db.backref('reservation', uselist=False))
    #annonce_id = db.Column(db.Integer, db.ForeignKey('annonces.ida'))  # Clé étrangère vers Annonce (restaurant)
    #annonce = db.relationship('Annonce', backref=db.backref('reservations', lazy=True))  # Relation avec Annonce

    def __init__(self,idr, horaire, user_id, table_idt):
        self.idr = idr,
        self.horaire = horaire
        self.user_id = user_id
        self.table_idt = table_idt

    @property
    def data(self):
        return {
            'idr': self.idr,
            'horaire': self.horaire,
            #'user': self.user.data,
            'table': self.table.data
        }
    
    def save(self):
        #from .user import User
        db.session.add(self)  
        db.session.commit() 

    