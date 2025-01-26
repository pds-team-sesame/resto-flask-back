from extensions import db

class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    restaurant_name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(255), nullable=True)
    gerent_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    gerent = db.relationship('User', back_populates='restaurants')
    menus = db.relationship('Menu', back_populates='restaurant', cascade='all, delete-orphan')
    tables = db.relationship('Table', back_populates='restaurant', cascade='all, delete-orphan')
    reservations = db.relationship('Reservation', back_populates='restaurant', cascade='all, delete-orphan')

    # Attacher to_dict comme méthode de la classe
    def to_dict(self):
        return {
            "id": self.id,
            "restaurant_name": self.restaurant_name,
            "address": self.address,
            "phone_number": self.phone_number,
            "description": self.description,
            "image_url": self.image_url,
        }
