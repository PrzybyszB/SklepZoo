from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, current_user
from flasgger import swag_from
from werkzeug.security import generate_password_hash, check_password_hash
from src.db_models import db, Users
import validators
from src.constant.https_status_code import HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT, HTTP_201_CREATED, HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_500_INTERNAL_SERVER_ERROR





api_user_blueprint = Blueprint('api_user_blueprint', __name__, static_folder="static", template_folder="templates")



@api_user_blueprint.post('/api/register')
@swag_from('/src/docs/swag_user/api_register.yml')
def api_add_user():
    
    try:
        name = request.json['name']
        last_name = request.json['last_name']
        username = request.json['username']
        email = request.json['email']
        password = request.json['password']
        password2 = request.json['password2']
        address = request.json['address']
        
    except KeyError as e:
        # Return an error response if any required data is missing.
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
@swag_from('/src/docs/swag_user/api_login.yml')
def api_login():

    email = request.json.get('email', '')
    password_hash = request.json.get('password', '')

    user = Users.query.filter_by(email=email).first()
    
    # Check if user exists.
    if user is None:
        return jsonify({'error' : "That user doeasn't exist"}), HTTP_400_BAD_REQUEST
    
    # If user exists, check password.
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
@swag_from('/src/docs/swag_user/api_logout.yml')
def api_logout():
    
    if not current_user.is_authenticated:
        return jsonify({'error' : "You are not log in"}), HTTP_401_UNAUTHORIZED
    else:
        logout_user()
        return jsonify({'response' : "You have been logged out"}), HTTP_200_OK


@api_user_blueprint.get('/api/user')
@swag_from('/src/docs/swag_user/api_dashboard.yml')
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
@swag_from('/src/docs/swag_user/api_update.yml')
def api_update():
    
    if not current_user.is_authenticated:
        return jsonify({'error' : "You are not log in"}), HTTP_401_UNAUTHORIZED
    
    if current_user.is_authenticated:
        try:
            # Get the user from the database based on current user's ID
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
                
                db.session.commit()
                
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
@swag_from('/src/docs/swag_user/api_user_list.yml')
def api_user_list():
    
    if not current_user.is_authenticated:
        return jsonify({'error' : "Oops u are not login as Admin"}), HTTP_401_UNAUTHORIZED 

     # Check if the current user is user_id = 1. Admin should be user with user_id = 1.
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

