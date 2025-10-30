import re
from flask import Blueprint, request, jsonify
from models import User, db
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({'msg': 'Email and password are required.'}), 400
    email = data['email'].strip()
    password = data['password']
    if not email or not password:
        return jsonify({'msg': 'Email and password cannot be empty.'}), 400
    if not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
        return jsonify({'msg': 'Invalid email format.'}), 400
    if len(password) < 6:
        return jsonify({'msg': 'Password must be at least 6 characters long.'}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({'msg': 'Already registered. Please login.'}), 409
    try:
        user = User(email=email)
        user.password = password  # Triggers password_hash property in your model
        db.session.add(user)
        db.session.commit()
        return jsonify({'msg': 'Registration successful. Please login.'}), 201
    except Exception as e:
        db.session.rollback()
        print('REGISTRATION ERROR:', e)
        return jsonify({'msg': f'Registration failed: {e}'}), 500
    
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if not user or not check_password_hash(user.password_hash, data['password']):
        return jsonify({'msg': 'Not registered, please register first.'}), 401
    access_token = create_access_token(identity=user.id)
    return jsonify({'token': access_token, 'msg': 'Login successful.'}), 200
