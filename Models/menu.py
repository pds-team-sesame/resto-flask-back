from extensions import db

# Table Menu
class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description_plat = db.Column(db.Text, nullable=True)
    photo = db.Column(db.String(255), nullable=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'))
    restaurant = db.relationship('Restaurant', back_populates='menus')

    def to_dict(self):
        return {
        "id": self.id,
        "name": self.name,
        "price": self.price,
        "description_plat": self.description_plat,
        "photo": self.photo,
        "restaurant_id": self.restaurant_id,
        "restaurant_name": self.restaurant.restaurant_name if self.restaurant else None
    }

