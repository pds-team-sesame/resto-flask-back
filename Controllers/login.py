from flask import request, jsonify
from Models.user import User
from werkzeug.security import check_password_hash

def login_function():
    try:
        # Récupérer les données JSON envoyées par le client
        data = request.json
        print(f"Received data: {data}")
        if not data:
            raise ValueError("Aucune donnée reçue")
        
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            raise ValueError("Nom d'utilisateur ou mot de passe manquant")

        # Vérifier si l'utilisateur existe
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            # Filtrer les données à envoyer, sans le mot de passe
            response_data = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.role.name  # Ne pas envoyer le mot de passe
            }
            print(f"Login successful for user: {username}")
            return response_data  # Retourner directement les données sous forme de dictionnaire
        else:
            print("Invalid username or password")
            return None  # Nom d'utilisateur ou mot de passe incorrect

    except Exception as e:
        print(f"Error during login: {str(e)}")
        return {"success": False, "message": str(e)}  # Retourner un dictionnaire d'erreur
