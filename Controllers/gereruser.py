from Models.user import User  # Modèle SQLAlchemy
def consulter():
    users = User.query.all()  # Récupère tous les utilisateurs
    return [user.to_dict() for user in users]

