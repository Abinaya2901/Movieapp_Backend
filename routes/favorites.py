from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Favorite, db

favorites_bp = Blueprint('favorites', __name__)

@favorites_bp.route('', methods=['GET'])
@jwt_required()
def get_favorites():
    user_id = get_jwt_identity()
    favs = Favorite.query.filter_by(user_id=user_id).all()
    return jsonify([f.movie_id for f in favs])

@favorites_bp.route('', methods=['POST'])
@jwt_required()
def add_favorite():
    user_id = get_jwt_identity()
    movie_id = request.json.get('movie_id')
    if Favorite.query.filter_by(user_id=user_id, movie_id=movie_id).first():
        return jsonify({'msg': 'Already in favorites'}), 409
    fav = Favorite(user_id=user_id, movie_id=movie_id)
    db.session.add(fav)
    db.session.commit()
    return jsonify({'msg': 'Added to favorites'}), 201

@favorites_bp.route('', methods=['DELETE'])
@jwt_required()
def remove_favorite():
    user_id = get_jwt_identity()
    movie_id = request.json.get('movie_id')
    fav = Favorite.query.filter_by(user_id=user_id, movie_id=movie_id).first()
    if fav:
        db.session.delete(fav)
        db.session.commit()
        return jsonify({'msg': 'Removed from favorites'}), 200
    return jsonify({'msg': 'Not found'}), 404
