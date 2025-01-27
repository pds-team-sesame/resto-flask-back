from extensions import db


class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    num_guests = db.Column(db.Integer, nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'))
    table_id = db.Column(db.Integer, db.ForeignKey('table.id'))
    client = db.relationship('User', back_populates='reservations')
    restaurant = db.relationship('Restaurant', back_populates='reservations')
    table = db.relationship('Table', back_populates='reservations')

    def to_dict(self):
        return {
            "id": self.id,
            "date": self.date.isoformat(),
            "num_guests": self.num_guests,
            "client_id": self.client_id,
            "restaurant_id": self.restaurant_id,
            "table_id": self.table_id
        }
