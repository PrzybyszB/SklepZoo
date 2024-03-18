from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from src.db_models import db, Users
import validators
from src.constant.https_status_code import HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT, HTTP_201_CREATED, HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_500_INTERNAL_SERVER_ERROR





api_user_blueprint = Blueprint('api_user_blueprint', __name__, static_folder="static", template_folder="templates")



@api_user_blueprint.post('/api/add_user')
def api_add_user():
    
    try:
        name = request.json['name']
        last_name = request.json.get('last_name', None)
        username = request.json['username']
        email = request.json['email']
        password = request.json['password']
        password2 = request.json['password2']
        address = request.json.get('address', None)
        
    except KeyError as e:
        return jsonify({'error': f"Missing data {e}"}), HTTP_400_BAD_REQUEST

    if not validators.email(email):
        return jsonify({'error': "Email is not valid"}), HTTP_400_BAD_REQUEST
    
    if password != password2:
        return jsonify({'error': "Password must match!"}), HTTP_400_BAD_REQUEST

    if Users.query.filter_by(email=email).first() is not None:
        return jsonify({'error': "Email is taken"}), HTTP_409_CONFLICT

    pwd_hash = generate_password_hash(password, "pbkdf2:sha256")

    user = Users(name=name,
                 last_name=last_name,
                 username=username, 
                 email=email, 
                 password_hash=pwd_hash, 
                 address=address )
    
    db.session.add(user)
    db.session.commit()

    return jsonify({
                    'message': "User created",
                    'user': {
                        'username': username, 
                        'email' : email
                    }}), HTTP_201_CREATED


@api_user_blueprint.post('/api/login')
def api_login():
    email = request.json.get('email', '')
    password_hash = request.json.get('password', '')

    user = Users.query.filter_by(email=email).first()
    
    if user is None:
        return jsonify({'error' : "That user doeasn't exist"}), HTTP_400_BAD_REQUEST
    
    if user:
        if check_password_hash(user.password_hash, password_hash):
            login_user(user)
            return jsonify({
                'user':{
                    'username' : user.username,
                    'email' : user.email
                }
            }), HTTP_200_OK
        else:
            return jsonify({'error' : "wrong password - Try again"}), HTTP_401_UNAUTHORIZED 


@api_user_blueprint.post('/api/logout')
def api_logout():
    if not current_user.is_authenticated:
        return jsonify({'error' : "You are not log in"}), HTTP_401_UNAUTHORIZED
    else:
        logout_user()
        return jsonify({'response' : "You have been logged out"}), HTTP_200_OK


@api_user_blueprint.get('/api/user')
def api_dashboard():
    if not current_user.is_authenticated:
        return jsonify({'error' : "You are not log in"}), HTTP_401_UNAUTHORIZED 
    else:
        return jsonify({
            'user':{
                'username' : current_user.username,
                'email' : current_user.email,
                'address' : current_user.address,
                'last_name' : current_user.last_name,
            }
        }), HTTP_200_OK


@api_user_blueprint.route('/api/user', methods=['PUT'])
def api_update():
    if not current_user.is_authenticated:
        return jsonify({'error' : "You are not log in"}), HTTP_401_UNAUTHORIZED
    
    if current_user.is_authenticated:
        try:
            user = Users.query.get(current_user.user_id)
            if user:
                if 'name' in request.json:
                    user.name = request.json['name']
                if 'username' in request.json:
                    user.username = request.json['username']
                if 'last_name' in request.json:
                    user.last_name = request.json['last_name']
                if 'address' in request.json:
                    user.address = request.json['address']
                return jsonify({ 
                    'response' : 'user updated',
                    'user' : {
                        "name" : user.name,
                        "username" : user.username,
                        "last_name" : user.last_name,
                        "address" : user.address

                    }}), HTTP_200_OK
        except:
            return jsonify({'resposne' : 'error updating user'}), HTTP_500_INTERNAL_SERVER_ERROR
        
@api_user_blueprint.get('/api/user-list')
def api_user_list():
    if not current_user.is_authenticated:
        return jsonify({'error' : "Oops u are not login as Admin"}), HTTP_401_UNAUTHORIZED 

    if current_user.is_authenticated:
        id = current_user.user_id
        if id == 1:
            our_users = Users.query.order_by(Users.email)
            user_list = []
            
            for our_user in our_users:
                username = our_user.username
                name = our_user.name
                last_name = our_user.last_name
                email = our_user.email
                address = our_user.address

                user_list.append({
                    "username" : username,
                    "name" : name,
                    "last_name" : last_name,
                    "email" : email,
                    "address" : address})
            
            return jsonify({"user list" : user_list}), HTTP_200_OK
        
        
        else:
            return jsonify({'error' : "You are not Admin"}), HTTP_401_UNAUTHORIZED 

