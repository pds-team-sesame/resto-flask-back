from flask import request, jsonify
from Models.user import User
from Models.role import Role  # Assurez-vous que Role est bien importé
from extensions import db
from werkzeug.security import generate_password_hash

def register_function():
    try:
        # Récupérer les données JSON envoyées par le client
        data = request.json
        print(f"Received data: {data}")  # Log des données reçues

        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        role = data.get('role')

        # Validation des champs obligatoires
        if not username or not email or not password or not role:
            return jsonify({"success": False, "message": "Tous les champs sont requis"}), 400

        # Vérifier que le rôle est valide
        if role not in Role._value2member_map_:
            print(f"Invalid role: {role}")  # Log du rôle invalide
            return jsonify({"success": False, "message": "Rôle invalide"}), 400

        # Convertir le rôle (chaîne) en membre de l'énumération
        role_enum = Role[role.upper()]  # Utiliser .upper() si vous envoyez le rôle en minuscules

        # Hasher le mot de passe avant de l'enregistrer
        hashed_password = generate_password_hash(password)

        # Créer un nouvel utilisateur avec le rôle validé
        user = User(
            username=username,
            email=email,
            password=hashed_password,
            role=role_enum  # Utiliser l'énumération Role
        )

        # Ajouter l'utilisateur à la base de données
        db.session.add(user)
        db.session.commit()

        # Préparer la réponse sans le mot de passe
        response_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role.name  # Utiliser le nom du rôle (pas l'objet)
        }

        return jsonify({"success": True, "message": "Inscription réussie", "data": response_data}), 201

    except Exception as e:
        print(f"Error during registration: {str(e)}")  # Log l'erreur
        return jsonify({"success": False, "message": str(e)}), 400
