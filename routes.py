from flask import Blueprint, make_response, request, jsonify, flash
from Controllers.register import register_function
from Controllers.login import login_function
from Controllers.gereruser import consulter 
from werkzeug.security import generate_password_hash
from Models.user import User
from Models.role import Role
from Models.restaurant import Restaurant
from Models.menu import Menu
from Models.commande import Commande
from Models.table import Table
from Models.reservation import Reservation
from Models.livraison import Livraison
from Models.paiement import Paiement
from Models.avis import Avis
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



#---------------Partie CRUD Menu----------------------------------

# Route pour ajouter un menu
@main.route('/api/menu', methods=['POST'])
def add_menu():
    try:
        if not request.is_json:
            return jsonify({"error": "Invalid content type. Please use application/json."}), 415

        data = request.get_json()

        required_fields = ['name', 'price', 'restaurant_id']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400

        new_menu = Menu(
            name=data['name'],
            price=data['price'],
            description_plat=data.get('description_plat', ''),
            photo=data.get('photo', None),
            restaurant_id=data['restaurant_id']
        )

        db.session.add(new_menu)
        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Menu added successfully",
            "menu": new_menu.to_dict()
        }), 201

    except Exception as e:
        print(f"Erreur: {str(e)}")
        return jsonify({"error": "Internal server error", "message": str(e)}), 500


# Route pour afficher tous les menus
@main.route('/api/getAllmenus', methods=['GET'])
def get_all_menus():
    menus = Menu.query.all()
    menus_list = [menu.to_dict() for menu in menus]
    return jsonify(menus_list), 200


# Route pour afficher un menu par ID
@main.route('/api/getmenu/<int:id>', methods=['GET'])
def get_menu_by_id(id):
    menu = Menu.query.get(id)
    if not menu:
        return jsonify({"error": "Menu not found"}), 404

    return jsonify(menu.to_dict()), 200


# Route pour supprimer un menu
@main.route('/api/supmenu/<int:id>', methods=['DELETE'])
def delete_menu(id):
    menu = Menu.query.get(id)
    if not menu:
        return jsonify({"error": "Menu not found"}), 404

    db.session.delete(menu)
    db.session.commit()
    return jsonify({"message": "Menu deleted successfully"}), 200


# Route pour modifier un menu
@main.route('/api/modifmenu/<int:id>', methods=['PUT'])
def update_menu(id):
    try:
        if not request.is_json:
            return jsonify({"error": "Invalid content type. Please use application/json."}), 415

        data = request.get_json()

        menu = Menu.query.get(id)
        if not menu:
            return jsonify({"error": "Menu not found"}), 404

        menu.name = data['name']
        menu.price = data['price']
        menu.description_plat = data.get('description_plat', menu.description_plat)
        menu.photo = data.get('photo', menu.photo)
        menu.restaurant_id = data['restaurant_id']

        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Menu updated successfully",
            "menu": menu.to_dict()
        }), 200

    except Exception as e:
        print(f"Erreur: {str(e)}")
        return jsonify({"error": "Internal server error", "message": str(e)}), 500



#---------------Partie CRUD Commande----------------------------------

# Route pour ajouter une commande
@main.route('/api/add-commande', methods=['POST'])
def add_commande():
    try:
        if not request.is_json:
            return jsonify({"error": "Invalid content type. Please use application/json."}), 415

        data = request.get_json()

        required_fields = ['client_id', 'restaurant_id']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400

        new_commande = Commande(
            client_id=data['client_id'],
            restaurant_id=data['restaurant_id']
        )

        db.session.add(new_commande)
        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Commande added successfully",
            "commande": new_commande.to_dict()
        }), 201

    except Exception as e:
        print(f"Erreur: {str(e)}")
        return jsonify({"error": "Internal server error", "message": str(e)}), 500


# Route pour afficher toutes les commandes
@main.route('/api/getAllcommandes', methods=['GET'])
def get_all_commandes():
    commandes = Commande.query.all()
    commandes_list = [commande.to_dict() for commande in commandes]
    return jsonify(commandes_list), 200


# Route pour afficher une commande par ID
@main.route('/api/getcommande/<int:id>', methods=['GET'])
def get_commande_by_id(id):
    commande = Commande.query.get(id)
    if not commande:
        return jsonify({"error": "Commande not found"}), 404

    return jsonify(commande.to_dict()), 200


# Route pour supprimer une commande
@main.route('/api/delete-commande/<int:id>', methods=['DELETE'])
def delete_commande(id):
    commande = Commande.query.get(id)
    if not commande:
        return jsonify({"error": "Commande not found"}), 404

    db.session.delete(commande)
    db.session.commit()
    return jsonify({"message": "Commande deleted successfully"}), 200


# Route pour modifier une commande
@main.route('/api/update-commande/<int:id>', methods=['PUT'])
def update_commande(id):
    try:
        if not request.is_json:
            return jsonify({"error": "Invalid content type. Please use application/json."}), 415

        data = request.get_json()

        commande = Commande.query.get(id)
        if not commande:
            return jsonify({"error": "Commande not found"}), 404

        commande.client_id = data['client_id']
        commande.restaurant_id = data['restaurant_id']

        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Commande updated successfully",
            "commande": commande.to_dict()
        }), 200

    except Exception as e:
        print(f"Erreur: {str(e)}")
        return jsonify({"error": "Internal server error", "message": str(e)}), 500



#-----------Partie CRUD Table -------------------------
@main.route('/api/add-table', methods=['POST'])
def add_table():
    try:
        if not request.is_json:
            return jsonify({"error": "Invalid content type. Please use application/json."}), 415

        data = request.get_json()

        required_fields = ['number', 'capacity', 'restaurant_id']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400

        new_table = Table(
            number=data['number'],
            capacity=data['capacity'],
            restaurant_id=data['restaurant_id']
        )

        db.session.add(new_table)
        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Table added successfully",
            "table": new_table.to_dict()
        }), 201

    except Exception as e:
        print(f"Erreur: {str(e)}")
        return jsonify({"error": "Internal server error", "message": str(e)}), 500

@main.route('/api/getAlltables', methods=['GET'])
def get_tables():
    try:
        tables = Table.query.all()
        tables_list = [table.to_dict() for table in tables]
        return jsonify(tables_list), 200
    except Exception as e:
        print(f"Erreur: {str(e)}")
        return jsonify({"error": "Internal server error", "message": str(e)}), 500

@main.route('/api/getable/<int:id>', methods=['GET'])
def get_table_by_id(id):
    try:
        table = Table.query.get(id)
        if not table:
            return jsonify({"error": "Table not found"}), 404
        return jsonify(table.to_dict()), 200
    except Exception as e:
        print(f"Erreur: {str(e)}")
        return jsonify({"error": "Internal server error", "message": str(e)}), 500

@main.route('/api/modifiertable/<int:id>', methods=['PUT'])
def update_table(id):
    try:
        if not request.is_json:
            return jsonify({"error": "Invalid content type. Please use application/json."}), 415

        data = request.get_json()
        table = Table.query.get(id)
        if not table:
            return jsonify({"error": "Table not found"}), 404

        table.number = data.get('number', table.number)
        table.capacity = data.get('capacity', table.capacity)
        table.restaurant_id = data.get('restaurant_id', table.restaurant_id)

        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Table updated successfully",
            "table": table.to_dict()
        }), 200

    except Exception as e:
        print(f"Erreur: {str(e)}")
        return jsonify({"error": "Internal server error", "message": str(e)}), 500

@main.route('/api/supptable/<int:id>', methods=['DELETE'])
def delete_table(id):
    try:
        table = Table.query.get(id)
        if not table:
            return jsonify({"error": "Table not found"}), 404

        db.session.delete(table)
        db.session.commit()
        return jsonify({"message": "Table deleted successfully"}), 200
    except Exception as e:
        print(f"Erreur: {str(e)}")
        return jsonify({"error": "Internal server error", "message": str(e)}), 500



# ---------------- Prtie CRUD Reservation ------------------

# Route pour ajouter une réservation
@main.route('/api/add-reservation', methods=['POST'])
def add_reservation():
    try:
        if not request.is_json:
            return jsonify({"error": "Invalid content type. Please use application/json."}), 415

        data = request.get_json()

        required_fields = ['date', 'num_guests', 'client_id', 'restaurant_id', 'table_id']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400

        new_reservation = Reservation(
            date=data['date'],
            num_guests=data['num_guests'],
            client_id=data['client_id'],
            restaurant_id=data['restaurant_id'],
            table_id=data['table_id']
        )

        db.session.add(new_reservation)
        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Reservation added successfully",
            "reservation": new_reservation.to_dict()
        }), 201

    except Exception as e:
        print(f"Erreur: {str(e)}")
        return jsonify({"error": "Internal server error", "message": str(e)}), 500


# Route pour afficher toutes les réservations
@main.route('/api/getAllreservations', methods=['GET'])
def get_all_reservations():
    reservations = Reservation.query.all()
    reservations_list = [reservation.to_dict() for reservation in reservations]
    return jsonify(reservations_list), 200


# Route pour afficher une réservation par ID
@main.route('/api/getreservation/<int:id>', methods=['GET'])
def get_reservation_by_id(id):
    reservation = Reservation.query.get(id)
    if not reservation:
        return jsonify({"error": "Reservation not found"}), 404

    return jsonify(reservation.to_dict()), 200


# Route pour supprimer une réservation
@main.route('/api/delete-reservation/<int:id>', methods=['DELETE'])
def delete_reservation(id):
    reservation = Reservation.query.get(id)
    if not reservation:
        return jsonify({"error": "Reservation not found"}), 404

    db.session.delete(reservation)
    db.session.commit()
    return jsonify({"message": "Reservation deleted successfully"}), 200


# Route pour modifier une réservation
@main.route('/api/update-reservation/<int:id>', methods=['PUT'])
def update_reservation(id):
    try:
        if not request.is_json:
            return jsonify({"error": "Invalid content type. Please use application/json."}), 415

        data = request.get_json()

        reservation = Reservation.query.get(id)
        if not reservation:
            return jsonify({"error": "Reservation not found"}), 404

        reservation.date = data['date']
        reservation.num_guests = data['num_guests']
        reservation.client_id = data['client_id']
        reservation.restaurant_id = data['restaurant_id']
        reservation.table_id = data['table_id']

        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Reservation updated successfully",
            "reservation": reservation.to_dict()
        }), 200

    except Exception as e:
        print(f"Erreur: {str(e)}")
        return jsonify({"error": "Internal server error", "message": str(e)}), 500

# ------------------ Les CRUD de livraison -------------------------
@main.route('/api/add-livraison', methods=['POST'])
def add_livraison():
    try:
        if not request.is_json:
            return jsonify({"error": "Invalid content type. Please use application/json."}), 415

        data = request.get_json()

        required_fields = ['date','status', 'commande_id', 'livreur_id']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400

        new_livraison = Livraison(
            date= data['date'],
            status=data['status'],
            commande_id=data['commande_id'],
            livreur_id=data['livreur_id']
        )

        db.session.add(new_livraison)
        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Livraison added successfully",
            "livraison": new_livraison.to_dict()
        }), 201

    except Exception as e:
        print(f"Erreur: {str(e)}")
        return jsonify({"error": "Internal server error", "message": str(e)}), 500

@main.route('/api/getAlllivraisons', methods=['GET'])
def get_livraisons():
    try:
        livraisons = Livraison.query.all()
        livraisons_list = [livraison.to_dict() for livraison in livraisons]
        return jsonify(livraisons_list), 200
    except Exception as e:
        print(f"Erreur: {str(e)}")
        return jsonify({"error": "Internal server error", "message": str(e)}), 500

@main.route('/api/getlivraison/<int:id>', methods=['GET'])
def get_livraison_by_id(id):
    try:
        livraison = Livraison.query.get(id)
        if not livraison:
            return jsonify({"error": "Livraison not found"}), 404
        return jsonify(livraison.to_dict()), 200
    except Exception as e:
        print(f"Erreur: {str(e)}")
        return jsonify({"error": "Internal server error", "message": str(e)}), 500

@main.route('/api/modiflivraison/<int:id>', methods=['PUT'])
def update_livraison(id):
    try:
        if not request.is_json:
            return jsonify({"error": "Invalid content type. Please use application/json."}), 415

        data = request.get_json()
        livraison = Livraison.query.get(id)
        if not livraison:
            return jsonify({"error": "Livraison not found"}), 404
        livraison.date = data.get('date',livraison.date),
        livraison.status = data.get('status', livraison.status)
        livraison.commande_id = data.get('commande_id', livraison.commande_id)
        livraison.livreur_id = data.get('livreur_id', livraison.livreur_id)

        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Livraison updated successfully",
            "livraison": livraison.to_dict()
        }), 200

    except Exception as e:
        print(f"Erreur: {str(e)}")
        return jsonify({"error": "Internal server error", "message": str(e)}), 500

@main.route('/api/supplivraison/<int:id>', methods=['DELETE'])
def delete_livraison(id):
    try:
        livraison = Livraison.query.get(id)
        if not livraison:
            return jsonify({"error": "Livraison not found"}), 404

        db.session.delete(livraison)
        db.session.commit()
        return jsonify({"message": "Livraison deleted successfully"}), 200
    except Exception as e:
        print(f"Erreur: {str(e)}")
        return jsonify({"error": "Internal server error", "message": str(e)}), 500
# ------------------ Les CRUD de paiements-------------------------

@main.route('/api/add-paiement', methods=['POST'])
def add_paiement():
    try:
        if not request.is_json:
            return jsonify({"error": "Invalid content type. Please use application/json."}), 415

        data = request.get_json()

        required_fields = ['date','amount', 'status', 'commande_id']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400

        new_paiement = Paiement(
            date=data['date'],
            amount=data['amount'],
            status=data['status'],
            commande_id=data['commande_id']
        )

        db.session.add(new_paiement)
        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Paiement added successfully",
            "paiement": new_paiement.to_dict()
        }), 201

    except Exception as e:
        print(f"Erreur: {str(e)}")
        return jsonify({"error": "Internal server error", "message": str(e)}), 500

@main.route('/api/getAllpaiements', methods=['GET'])
def get_paiements():
    try:
        paiements = Paiement.query.all()
        paiements_list = [paiement.to_dict() for paiement in paiements]
        return jsonify(paiements_list), 200
    except Exception as e:
        print(f"Erreur: {str(e)}")
        return jsonify({"error": "Internal server error", "message": str(e)}), 500

@main.route('/api/getpaiement/<int:id>', methods=['GET'])
def get_paiement_by_id(id):
    try:
        paiement = Paiement.query.get(id)
        if not paiement:
            return jsonify({"error": "Paiement not found"}), 404
        return jsonify(paiement.to_dict()), 200
    except Exception as e:
        print(f"Erreur: {str(e)}")
        return jsonify({"error": "Internal server error", "message": str(e)}), 500

@main.route('/api/update-paiement/<int:id>', methods=['PUT'])
def update_paiement(id):
    try:
        if not request.is_json:
            return jsonify({"error": "Invalid content type. Please use application/json."}), 415

        data = request.get_json()
        paiement = Paiement.query.get(id)
        if not paiement:
            return jsonify({"error": "Paiement not found"}), 404
        paiement.date = data.get('date',paiement.date)
        paiement.amount = data.get('amount', paiement.amount)
        paiement.status = data.get('status', paiement.status)
        paiement.commande_id = data.get('commande_id', paiement.commande_id)

        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Paiement updated successfully",
            "paiement": paiement.to_dict()
        }), 200

    except Exception as e:
        print(f"Erreur: {str(e)}")
        return jsonify({"error": "Internal server error", "message": str(e)}), 500

@main.route('/api/delete-paiement/<int:id>', methods=['DELETE'])
def delete_paiement(id):
    try:
        paiement = Paiement.query.get(id)
        if not paiement:
            return jsonify({"error": "Paiement not found"}), 404

        db.session.delete(paiement)
        db.session.commit()
        return jsonify({"message": "Paiement deleted successfully"}), 200
    except Exception as e:
        print(f"Erreur: {str(e)}")
        return jsonify({"error": "Internal server error", "message": str(e)}), 500

# ------------------ Les CRUD des avis -------------------------

@main.route('/api/add-avis', methods=['POST'])
def add_avis():
    try:
        if not request.is_json:
            return jsonify({"error": "Invalid content type. Please use application/json."}), 415

        data = request.get_json()
        required_fields = ['commentaire', 'rating', 'date','status','commande_id', 'client_id','admin_id']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400

        # Vérifier si la commande et le client existent
        commande = Commande.query.get(data['commande_id'])
        client = User.query.get(data['client_id'])

        if not commande:
            return jsonify({"error": "Invalid commande_id. The specified commande does not exist."}), 400

        if not client:
            return jsonify({"error": "Invalid client_id. The specified client does not exist."}), 400

        # Créer un nouvel avis
        new_avis = Avis(
            commentaire=data['commentaire'],
            rating=data['rating'],
            date=data['date'],
            commande_id=data['commande_id'],
            client_id=data['client_id'],
            status=data.get('status', 'en attente')
        )

        db.session.add(new_avis)
        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Avis added successfully",
            "avis": new_avis.to_dict()
        }), 201

    except Exception as e:
        print(f"Erreur: {str(e)}")
        return jsonify({"error": "Internal server error", "message": str(e)}), 500

# Récupérer tous les avis
@main.route('/api/getAllaviss', methods=['GET'])
def get_all_avis():
    try:
        avis_list = Avis.query.all()
        return jsonify([avis.to_dict() for avis in avis_list]), 200
    except Exception as e:
        print(f"Erreur: {str(e)}")
        return jsonify({"error": "Internal server error", "message": str(e)}), 500

# Récupérer un avis par ID
@main.route('/api/getavis/<int:id>', methods=['GET'])
def get_avis_by_id(id):
    try:
        avis = Avis.query.get(id)
        if not avis:
            return jsonify({"error": "Avis not found"}), 404
        return jsonify(avis.to_dict()), 200
    except Exception as e:
        print(f"Erreur: {str(e)}")
        return jsonify({"error": "Internal server error", "message": str(e)}), 500

# Mettre à jour un avis
@main.route('/api/update-avis/<int:id>', methods=['PUT'])
def update_avis(id):
    try:
        if not request.is_json:
            return jsonify({"error": "Invalid content type. Please use application/json."}), 415

        data = request.get_json()
        avis = Avis.query.get(id)
        if not avis:
            return jsonify({"error": "Avis not found"}), 404

        avis.commentaire = data.get('commentaire', avis.commentaire)
        avis.rating = data.get('rating', avis.rating)
        avis.status = data.get('status', avis.status)
        avis.admin_id = data.get('admin_id', avis.admin_id)

        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Avis updated successfully",
            "avis": avis.to_dict()
        }), 200

    except Exception as e:
        print(f"Erreur: {str(e)}")
        return jsonify({"error": "Internal server error", "message": str(e)}), 500

# Supprimer un avis
@main.route('/api/delete-avis/<int:id>', methods=['DELETE'])
def delete_avis(id):
    try:
        avis = Avis.query.get(id)
        if not avis:
            return jsonify({"error": "Avis not found"}), 404

        db.session.delete(avis)
        db.session.commit()

        return jsonify({"message": "Avis deleted successfully"}), 200

    except Exception as e:
        print(f"Erreur: {str(e)}")
        return jsonify({"error": "Internal server error", "message": str(e)}), 500
