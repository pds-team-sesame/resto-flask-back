from extensions import db

class Menu(db.Model):
    __tablename__ = 'menus'
    
    idm = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description_plat = db.Column(db.String(100), nullable=False)
    photo = db.Column(db.String(255), nullable=True)  # Changer LargeBinary en String pour le chemin de fichier

    def __init__(self, name, price, description_plat, photo=None):
        self.name = name
        self.price = price
        self.description_plat = description_plat
        self.photo = photo

    @property
    def data(self):
        return {
            'idm': self.idm,
            'name': self.name,
            'price': self.price,
            'description_plat': self.description_plat,
            'photo': self.photo
        }
    
    def save(self):
        db.session.add(self)  
        db.session.commit() 