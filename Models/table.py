from extensions import db

class Table(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(10), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'))
    restaurant = db.relationship('Restaurant', back_populates='tables')
    reservations = db.relationship('Reservation', back_populates='table', cascade='all, delete-orphan')
