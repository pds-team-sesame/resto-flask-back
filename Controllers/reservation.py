from flask import request, jsonify
from extensions import db
from Models.reservation import Reservation
from Models.user import User
from Models.table import Table

def add_reservation_function():
    # Importation des modèles uniquement au moment de l'utilisation pour éviter les imports circulaires
    
    
    if request.method == "POST":
        # Vérification des données entrantes
        horaire = request.form.get('horaire')
        user_id = request.form.get('user')
        table_id = request.form.get('table')

        if not horaire or not user_id or not table_id:
            return jsonify({"error": "Tous les champs sont requis (horaire, user, table)."}), 400

        try:
            # Valider l'existence de l'utilisateur et de la table
            user = User.query.get(user_id)
            table = Table.query.get(table_id)
            
            if not user:
                return jsonify({"error": "Utilisateur non trouvé"}), 404
            
            if not table:
                return jsonify({"error": "Table non trouvée"}), 404

            # Créer une nouvelle réservation
            reservation = Reservation(
                horaire=horaire,
                user_id=user.id,
                table_id=table.id
            )
            
            # Ajouter la réservation à la session et sauvegarder
            db.session.add(reservation)
            db.session.commit()

            # Retourner les données au format JSON
            data = {
                'id': reservation.id,
                'horaire': reservation.horaire,
                'user': user.username,  # Si vous voulez retourner l'username
                'table': table.num       # Si vous voulez retourner le numéro de la table
            }
            return jsonify(data), 201

        except Exception as e:
            db.session.rollback()  # Annuler en cas d'erreur
            return jsonify({"error": str(e)}), 500
