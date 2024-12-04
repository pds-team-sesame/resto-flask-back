from extensions import db

class Table(db.Model):
    __tablename__ = 'table'
    
    idt = db.Column(db.Integer, primary_key=True)
    nb_place =db.Column(db.Integer, nullable=False)
    etat = db.Column(db.String(80), nullable=False)

    def __init__(self, idt, num):
        self.idt = idt
        self.num = num

    @property
    def data(self):
        return {
            'idt': self.idt,
            'num': self.num
        }
 

    def save(self):
        db.session.add(self)  
        db.session.commit() 