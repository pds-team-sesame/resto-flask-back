from extensions import db


class Avis(db.Model):
    __tablename__ = 'avis'
    
    id = db.Column(db.Integer, primary_key=True)
    commentaire = db.Column(db.String(255), nullable=False)

    # One-to-Many relationship with User
    #user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    #user = db.relationship('User', backref='avis')

    def __init__(self, commentaire ):
        self.commentaire = commentaire
       # self.user_id = user_id

    @property
    def data(self):
        return {
            'id': self.id,
            'commentaire': self.commentaire,
            #'user': self.user.data
        }
    def save(self):
        from .user import User
        db.session.add(self)  
        db.session.commit() 
