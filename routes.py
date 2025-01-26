from flask import Blueprint, make_response, request, jsonify, flash
from Controllers.register import register_function
from Controllers.login import login_function
from Controllers.gereruser import consulter 
from werkzeug.security import generate_password_hash
from Models.user import User
from Models.role import Role
from Models.restaurant import Restaurant
from extensions import db
main = Blueprint('main', __name__)

#------------ Register-------------------
@main.route('/api/register', methods=['POST'])
def register_user():
    try:
        # Appelle la fonction d'inscription
        data = register_function()  # Cette fonction renvoie déjà une réponse JSON
        return data  # Retourner la réponse venant de register_function
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400


# ----------- Login ---------------------
@main.route('/api/login', methods=['POST'])
def login_user():
    try:
        data = login_function()  # Appelle la fonction de traitement de connexion
        if data:  # Si les informations sont correctes
            return jsonify({"success": True, "message": "Connexion réussie", "user": data}), 200
        else:
            return jsonify({"success": False, "message": "Nom d'utilisateur ou mot de passe incorrect"}), 401
    except Exception as e:
        print(f"Error in login route: {str(e)}")  # Log de l'erreur dans la route
        return jsonify({"success": False, "message": str(e)}), 500

# ----------- consulter user ---------------------
@main.route('/api/gereruser', methods=['GET'])
def gerer_user():
    try:
        data = consulter()  # Appelle la fonction pour récupérer les utilisateurs
        if data:
            return jsonify({"success": True, "users": data}), 200
        else:
            return jsonify({"success": True, "users": []}), 200  # Si aucun utilisateur trouvé
    except Exception as e:
        print(f"Error in gerer_user route: {str(e)}")  # Log de l'erreur
        return jsonify({"success": False, "message": str(e)}), 500


# ----------- Récupérer les données d'un utilisateur par ID ---------------------
@main.route('/api/utilisateur/<int:id>', methods=['GET'])
def get_user_by_id(id):
    try:
        user = User.query.get(id)
        if not user:
            return jsonify({"success": False, "message": "Utilisateur non trouvé"}), 404

        # Ne pas inclure le champ 'password' dans la réponse
        user_data = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "password":user.password,
            "role": user.role.name  # Assuming 'Role' is an Enum or has a name attribute
        }

        return jsonify({
            "success": True,
            "user": user_data
        }), 200

    except Exception as e:
        print(f"Erreur: {str(e)}")
        return jsonify({"success": False, "message": str(e)}), 500


# ----------- Modifier un utilisateur par ID ---------------------
@main.route('/api/modifier/<int:id>', methods=['PUT'])
def update_user(id):
    try:
        data = request.get_json()

        # Validation du rôle
        valid_roles = ['client', 'admin', 'livreur', 'gerant']
        if data['role'] not in valid_roles:
            return jsonify({"success": False, "message": "Rôle invalide"}), 400
        
        user = User.query.get(id)
        if not user:
            return jsonify({"success": False, "message": "Utilisateur non trouvé"}), 404

        user.username = data['username']
        user.email = data['email']
        user.password = generate_password_hash(data['password'])
        user.role = Role[data['role'].upper()]  # Mettez à jour le rôle en utilisant l'énumération

        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Utilisateur mis à jour avec succès",
            "user": user.to_dict()  # Retourner les données de l'utilisateur sérialisées
        }), 200

    except Exception as e:
        print(f"Erreur: {str(e)}")
        return jsonify({"success": False, "message": str(e)}), 500


# ----------- Supprimer un utilisateur par ID ---------------------
@main.route('/api/supprimer/<int:id>', methods=['DELETE'])
def delete_user(id):
    try:
        user = User.query.get(id)
        if not user:
            return jsonify({"success": False, "message": "Utilisateur non trouvé"}), 404

        db.session.delete(user)
        db.session.commit()

        return jsonify({"success": True, "message": "Utilisateur supprimé avec succès"}), 200

    except Exception as e:
        print(f"Erreur: {str(e)}")
        return jsonify({"success": False, "message": str(e)}), 500

#------------- Partie CRUD Resto ------------------------------------
@main.route('/api/restaurant', methods=['POST'])
def add_restaurant():
    try:
        # Vérifiez si le type de contenu est JSON
        if not request.is_json:
            return jsonify({"error": "Invalid content type. Please use application/json."}), 415

        # Récupérer les données JSON
        data = request.get_json()

        # Valider les données obligatoires
        required_fields = ['restaurant_name', 'address', 'phone_number']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400

        # Vérifier et corriger l'URL de l'image (facultatif)
        image_url = data.get('image_url', None)
        if image_url and not (image_url.startswith('http://') or image_url.startswith('https://')):
            return jsonify({"error": "Invalid image_url. Must start with http:// or https://"}), 400

        # Créer un nouvel objet Restaurant
        new_restaurant = Restaurant(
            restaurant_name=data['restaurant_name'],
            address=data['address'],
            phone_number=data['phone_number'],
            description=data.get('description', ''),  # Valeur par défaut : chaîne vide
            image_url=image_url
        )

        # Ajouter et valider dans la base de données
        db.session.add(new_restaurant)
        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Restaurant added successfully",
            "restaurant": new_restaurant.to_dict()
        }), 201

    except Exception as e:
        print(f"Erreur: {str(e)}")
        return jsonify({"error": "Internal server error", "message": str(e)}), 500

# Route pour afficher tous les restaurants
@main.route('/api/getAllRestos', methods=['GET'])
def get_restaurants():
    restaurants = Restaurant.query.all()
    restaurants_list = [
        {
            "id": restaurant.id,
            "restaurant_name": restaurant.restaurant_name,
            "address": restaurant.address,
            "phone_number": restaurant.phone_number,
            "description": restaurant.description,
            "image_url": restaurant.image_url
        }
        for restaurant in restaurants
    ]
    return jsonify(restaurants_list), 200

# Route pour afficher un restaurant par ID
@main.route('/api/getRestos/<int:id>', methods=['GET'])
def get_restaurant_by_id(id):
    restaurant = Restaurant.query.get(id)
    if not restaurant:
        return jsonify({"error": "Restaurant not found"}), 404

    restaurant_data = {
        "id": restaurant.id,
        "restaurant_name": restaurant.restaurant_name,
        "address": restaurant.address,
        "phone_number": restaurant.phone_number,
        "description": restaurant.description,
        "image_url": restaurant.image_url
    }
    return jsonify(restaurant_data), 200

# Route pour supprimer un restaurant
@main.route('/api/deleteresto/<int:id>', methods=['DELETE'])
def delete_restaurant(id):
    restaurant = Restaurant.query.get(id)
    if not restaurant:
        return jsonify({"error": "Restaurant not found"}), 404

    db.session.delete(restaurant)
    db.session.commit()
    return jsonify({"message": "Restaurant deleted successfully"}), 200

# Route pour modifier un restaurant
@main.route('/api/modifier_resto/<int:id>', methods=['PUT'])
def update_restaurant(id):
    try:
        # Si le Content-Type n'est pas 'application/json', on tente de lire le corps manuellement.
        if not request.is_json:
            return jsonify({"error": "Invalid content type. Please use application/json."}), 415

        data = request.get_json()

        restaurant = Restaurant.query.get(id)
        if not restaurant:
            return jsonify({"error": "Restaurant not found"}), 404

        restaurant.restaurant_name = data['restaurant_name']
        restaurant.address = data['address']
        restaurant.phone_number = data['phone_number']
        restaurant.description = data['description']
        restaurant.image_url = data['image_url']

        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Restaurant updated successfully",
            "restaurant": restaurant.to_dict()  # Retourner les données du restaurant mises à jour
        }), 200

    except Exception as e:
        print(f"Erreur: {str(e)}")
        return jsonify({"error": "Internal server error", "message": str(e)}), 500
