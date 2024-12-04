from extensions import db

class Role(db.Model):
    __tablename__ = 'role'
    
    idrole = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __init__(self, name):
        self.name = name

    @property
    def data(self):
        return {
            'idrole': self.id,
            'name': self.name
        }
    
    def save(self):
        db.session.add(self)  
        db.session.commit() 