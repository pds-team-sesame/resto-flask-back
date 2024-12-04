from extensions import db
from .facturation import Facturation

class Paiement(db.Model):
    __tablename__ = 'paiements'
    
    idpaiement = db.Column(db.Integer, primary_key=True)
    amount_paid = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.DateTime, nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)  
    #facturation_id = db.Column(db.Integer, db.ForeignKey('facturations.idfact'), nullable=False)
    
    # Relation avec Facturation
    #facturation = db.relationship('Facturation', backref='paiement', lazy=True)

    def __init__(self, amount_paid, payment_date, payment_method, facturation_id):
        self.amount_paid = amount_paid
        self.payment_date = payment_date
        self.payment_method = payment_method
        self.facturation_id = facturation_id

    @property
    def data(self):
        return {
            'idpaiement': self.idpaiement,
            'amount_paid': self.amount_paid,
            'payment_date': self.payment_date,
            'payment_method': self.payment_method,
            'facturation_id': self.facturation_id
        }

    def __repr__(self):
        return f'<Paiement {self.idpaiement} - {self.amount_paid} €>'
    
    def save(self):
        db.session.add(self)  
        db.session.commit() 