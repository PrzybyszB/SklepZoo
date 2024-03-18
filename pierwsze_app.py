from flask import Flask, render_template, flash, request, redirect, url_for, session, jsonify
from flask_migrate import Migrate
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
from flask_admin import Admin, AdminIndexView, expose, helpers
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import re
import stripe
import validators
from src.constant.https_status_code import HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT, HTTP_201_CREATED, HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND,HTTP_500_INTERNAL_SERVER_ERROR
# from db_models import db, init_db, Users, Products, Category, Orders, Orders_detail, Customer
# from views.cart_blueprint import cart_blueprint
# from views.user_blueprint import user_blueprint
# from views.product_blueprint import product_blueprint
# from views.payment_blueprint import payment_blueprint
# from views.views_blueprint import views_blueprint
# import os




'''---------------------------------   REST API   --------------------------------------------'''
# POMOCNE   https://www.youtube.com/watch?v=WFzRy8KVcrM&t=4262s&ab_channel=CryceTruly
#           https://www.youtube.com/watch?v=dkgRxBw_4no&ab_channel=Craftech





# @app.route('/api/test', methods=['GET', 'POST'])
# def test():
#     if request.method == 'GET':
#         return jsonify ({"response": "Get Request Called"})
#     elif request.method == 'POST':
#         req_Json = request.json
#         name = req_Json['name']
#         return jsonify({"response": "Hi " + name})


# @app.post('/api/add_user')
# def api_add_user():
#     name = request.json['name']
#     last_name = request.json['last_name']
#     username = request.json['username']
#     email = request.json['email']
#     password = request.json['password']
#     password2 = request.json['password2']
#     address = request.json['address']
    
#     if not validators.email(email):
#         return jsonify({'error': "Email is not valid"}), HTTP_400_BAD_REQUEST
    
#     if password != password2:
#         return jsonify({'error': "Password must match!"}), HTTP_400_BAD_REQUEST

#     if Users.query.filter_by(email=email).first() is not None:
#         return jsonify({'error': "Email is taken"}), HTTP_409_CONFLICT

#     pwd_hash = generate_password_hash(password, "pbkdf2:sha256")

#     user = Users(name=name,
#                  last_name=last_name,
#                  username=username, 
#                  email=email, 
#                  password=pwd_hash, 
#                  address=address )
    
#     db.session.add(user)
#     db.session.commit()

#     return jsonify({
#                     'message': "User created",
#                     'user': {
#                         'username': username, 
#                         'email' : email
#                     }}), HTTP_201_CREATED


# @app.post('/api/login')
# def api_login():
#     email = request.json.get('email', '')
#     password_hash = request.json.get('password', '')

#     user = Users.query.filter_by(email=email).first()
    
#     if user is None:
#         return jsonify({'error' : "That user doeasn't exist"}), HTTP_400_BAD_REQUEST
    
#     if user:
#         if check_password_hash(user.password_hash, password_hash):
#             login_user(user)
#             return jsonify({
#                 'user':{
#                     'username' : user.username,
#                     'email' : user.email
#                 }
#             }), HTTP_200_OK
#         else:
#             return jsonify({'error' : "wrong password - Try again"}), HTTP_401_UNAUTHORIZED 


# @app.post('/api/logout')
# def api_logout():
#     if not current_user.is_authenticated:
#         return jsonify({'error' : "You are not log in"}), HTTP_401_UNAUTHORIZED
#     else:
#         logout_user()
#         return jsonify({'response' : "You have been logged out"}), HTTP_200_OK


# @app.get('/api/user')
# def api_dashboard():
#     if not current_user.is_authenticated:
#         return jsonify({'error' : "You are not log in"}), HTTP_401_UNAUTHORIZED 
#     else:
#         return jsonify({
#             'user':{
#                 'username' : current_user.username,
#                 'email' : current_user.email,
#                 'address' : current_user.address,
#                 'last_name' : current_user.last_name,
#             }
#         }), HTTP_200_OK

# @app.route('/api/user', methods=['PUT'])
# def api_update():
#     if not current_user.is_authenticated:
#         return jsonify({'error' : "You are not log in"}), HTTP_401_UNAUTHORIZED
    
#     if current_user.is_authenticated:
#         try:
#             user = Users.query.get(current_user.user_id)
#             if user:
#                 if 'name' in request.json:
#                     user.name = request.json['name']
#                 if 'username' in request.json:
#                     user.username = request.json['username']
#                 if 'last_name' in request.json:
#                     user.last_name = request.json['last_name']
#                 if 'address' in request.json:
#                     user.address = request.json['address']
#                 return jsonify({ 
#                     'response' : 'user updated',
#                     'user' : {
#                         "name" : user.name,
#                         "username" : user.username,
#                         "last_name" : user.last_name,
#                         "address" : user.address

#                     }}), HTTP_200_OK
#         except:
#             return jsonify({'resposne' : 'error updating user'}), HTTP_500_INTERNAL_SERVER_ERROR
    

# @app.post('/api/category')
# def api_add_category():
#     if not current_user.is_authenticated:
#         return jsonify({'error' : "Oops u are not login as Admin"}), HTTP_401_UNAUTHORIZED 
    
#     if current_user.is_authenticated:
#         id = current_user.user_id
#         if id == 1:
#             category_name = request.json['category_name']
#             category_slug = request.json['category_slug']
#             check_exist_category =  Category.query.filter_by(category_name=category_name).first()
#             if check_exist_category is None:
#                 new_category = Category(category_name = category_name,
#                                         category_slug = category_slug)
#                 db.session.add(new_category)
#                 db.session.commit()
#                 return jsonify({
#                     'message': 'Category created',
#                     'category_name' : category_name,
#                     'category_slug' : category_slug
#                 }),  HTTP_201_CREATED
#             else:
#                 return jsonify({'error' : " This category is already exist"}), HTTP_409_CONFLICT 
#         else:
#             return jsonify({'error' : "You are not Admin"}), HTTP_401_UNAUTHORIZED 


# @app.delete('/api/category')
# def api_delete_category():
#     if not current_user.is_authenticated:
#         return jsonify({'error' : "Oops u are not login as Admin"}), HTTP_401_UNAUTHORIZED 

#     if current_user.is_authenticated:
#         id = current_user.user_id
#         if id == 1:
#             category_id = request.json['category_id']
#             category_to_delete = Category.query.get(category_id)
#             if category_to_delete is None:
#                 return jsonify({'error' : f'This category with ID: {category_id} does not exist'})
#             db.session.delete(category_to_delete)
#             db.session.commit()

#             return jsonify({'response' : "Category was deleted"}), HTTP_200_OK
#         else:
#             return jsonify({'error' : "You are not Admin"}), HTTP_401_UNAUTHORIZED 
    

# @app.get('/api/category')
# def api_category_list():
#     our_categories = Category.query.order_by(Category.category_id).all()
#     category_list = []

#     for our_category in our_categories:
#         category_name = our_category.category_name
#         category_slug = our_category.category_slug
#         category_id = our_category.category_id
#         category_list.append({
#                     "category_name" : category_name,
#                     "category_slug" : category_slug,
#                     "category_id" : category_id})
#     return jsonify({"category_list" : category_list}), HTTP_200_OK


# @app.post('/api/product')
# def api_add_product():
#     if not current_user.is_authenticated:
#         return jsonify({'error' : "Oops u are not login as Admin"}), HTTP_401_UNAUTHORIZED 

#     if current_user.is_authenticated:
#         id = current_user.user_id
#         if id == 1:
#             product_name = request.json['product_name']
#             cost = request.json['cost']
#             producer = request.json['producer']
#             category_id = request.json['category_id']
            
#             if Category.query.filter_by(category_id=category_id).first() is None:
#                 return jsonify({'error': "This category doesn't exist"}), HTTP_409_CONFLICT
            
#             check_exist_product = Products.query.filter_by(product_name=product_name, deleted_at=None).first()
#             if check_exist_product is None:
#                 new_product = Products(product_name=product_name,
#                                         cost = cost,
#                                         producer = producer,
#                                         category_id = category_id)
#                 db.session.add(new_product)
#                 db.session.commit()
#                 return jsonify({
#                     'message': 'Product added',
#                     'product' : {
#                                 "product name" : product_name,
#                                 "cost" : cost,
#                                 "producer" : producer,
#                                 "category id" : category_id
#                     }
#                 }),  HTTP_201_CREATED
#         else:
#             return jsonify({'error' : "You are not Admin"}), HTTP_401_UNAUTHORIZED 


# @app.delete('/api/product')
# def api_delete_product():
#     if not current_user.is_authenticated:
#         return jsonify({'error' : "Oops u are not login as Admin"}), HTTP_401_UNAUTHORIZED 

#     if current_user.is_authenticated:
#         id = current_user.user_id
#         if id == 1:
#             product_id = request.json['product_id']
#             product_to_delete = Products.query.filter_by(id=product_id, deleted_at=None).first()
#             if product_to_delete is None:
#                 return jsonify({'error' : f'This product with ID: {product_id} does not exist'})
#             product_to_delete.deleted_at = datetime.utcnow()
#             db.session.commit()

#             return jsonify({'response' : "Product was deleted"}), HTTP_200_OK
#         else:
#             return jsonify({'error' : "You are not Admin"}), HTTP_401_UNAUTHORIZED 


# @app.get('/api/product-list')
# def api_products():
#     our_products = Products.query.filter(Products.deleted_at == None).order_by(Products.data_added).all()
#     product_list = []
    
#     for our_product in our_products:
#                 product_name = our_product.product_name
#                 cost = our_product.cost
#                 producer = our_product.producer
#                 category_id = our_product.category_id

#                 product_list.append({
#                     "product_name" : product_name,
#                     "cost" : cost,
#                     "producer" : producer,
#                     "category_id" : category_id})
    
#     return jsonify({"product_list" : product_list}), HTTP_200_OK


# @app.get('/api/product')
# def api_product():
#     product_id = request.json['product_id']
#     product = Products.query.filter_by(product_id = product_id, deleted_at=None).first()
#     if product is None:
#         return jsonify({ 'error' : f'There is no product on product id {product_id}'}), HTTP_404_NOT_FOUND 
#     else:
#         return jsonify({
#                     'product info': {
#                         'product id' : product.product_id,
#                         'product name': product.product_name, 
#                         'cost' : product.cost,
#                         'producer' : product.producer,
#                         'category id' : product.category_id,
#                         'data added' : product.data_added.strftime("%Y-%m-%d %H:%M:%S")
#                     }}), HTTP_200_OK
    

# @app.get('/api/user-list')
# def api_user_list():
#     if not current_user.is_authenticated:
#         return jsonify({'error' : "Oops u are not login as Admin"}), HTTP_401_UNAUTHORIZED 

#     if current_user.is_authenticated:
#         id = current_user.user_id
#         if id == 1:
#             our_users = Users.query.order_by(Users.email)
#             user_list = []
            
#             for our_user in our_users:
#                 username = our_user.username
#                 name = our_user.name
#                 last_name = our_user.last_name
#                 email = our_user.email
#                 address = our_user.address

#                 user_list.append({
#                     "username" : username,
#                     "name" : name,
#                     "last_name" : last_name,
#                     "email" : email,
#                     "address" : address})
            
#             return jsonify({"user list" : user_list}), HTTP_200_OK
        
        
#         else:
#             return jsonify({'error' : "You are not Admin"}), HTTP_401_UNAUTHORIZED 


# @app.get('/api/cart')
# def api_cart():
#     cart = session.get('cart', [])
#     return jsonify({'cart' : cart}), HTTP_200_OK


# @app.post('/api/cart')
# def api_add_to_cart():
#     cart = session.get('cart', [])
#     if 'products' in request.json and isinstance(request.json['products'], list):
#             for product in request.json['products']:
#                 product_id = product.get('product_id')
#                 quantity = product.get('quantity')
#                 product = Products.query.get(product_id)
#                 if product:
#                     cart.append({'product_id': product_id, 'quantity': quantity})
#                 else:
#                     return jsonify({'error' : f'Product with id {product_id} was not found',
#                                     'cart' : cart}), HTTP_404_NOT_FOUND     
#     session['cart'] = cart
        
#     return jsonify({
#         'respone' : "Products was added successfully",
#         'cart': cart}), HTTP_200_OK
# '''
# {
#     "products": [
#         {
#             "product_id": "2",
#             "quantity": "3"
#         },
#         {
#             "product_id": "4",
#             "quantity": "1"
#         }
#     ]
# }
# '''


# @app.route('/api/cart', methods = ['PUT'])
# def api_update_cart():
#     cart = session.get('cart', [])
#     # If request is a list (more than one product)
#     if isinstance(request.json, list):
#         for item in request.json:
#             if 'product_id' in item and 'quantity' in item:
#                 product_id = item['product_id']
#                 quantity = item['quantity']
#                 product_found = False
#                 for key in cart:
#                     if key['product_id'] == product_id:
#                         key['quantity'] = quantity
#                         product_found = True
#                 if not product_found:
#                     return jsonify({'error': f'Product with ID: {product_id} was not found'}), HTTP_400_BAD_REQUEST
    
#     session['cart'] = cart
#     session.modified = True
#     return jsonify({'message': 'Cart updated successfully', 'cart': cart}), HTTP_200_OK




# @app.post('/api/customer_creator')
# def api_customer_creator():
#     if not current_user.is_authenticated:
#         name = request.json['name']
#         last_name = request.json['last_name']
#         email = request.json['email']
#         address = request.json['address']

#         if not validators.email(email):
#             return jsonify({'error': "Email is not valid"}), HTTP_400_BAD_REQUEST

#         customer_user = Customer(name = name,
#                                  last_name = last_name,
#                                  email = email,
#                                  address = address)
#         db.session.add(customer_user)
#         db.session.commit()
#         return jsonify({'respone' : 'customer was created',
#                         'customer' : {
#                             'name' : customer_user.name,
#                             'last_name' : customer_user.last_name,
#                             'email' : customer_user.email,
#                             'address' : customer_user.address
#                         }})
#     return jsonify({'error' : "You cant create a customer when u are log in"}), HTTP_400_BAD_REQUEST


# @app.post('/api/order')
# def api_order():
#     user_id = None
#     customer_id = None

#     if current_user.is_authenticated:
#         user_id = current_user.user_id
#     else:
#         customer_id = request.json['customer_id']
#         customer = Customer.query.get(customer_id)
#         if customer is None:
#             return jsonify({'error' : "That customer doesn't exist"}), HTTP_400_BAD_REQUEST
    
#     cart = session.get('cart')
#     if cart is None:
#         return jsonify({'error' : "Your cart is empty"}), HTTP_200_OK
    
#     if cart is not cart:
#         return jsonify({'error' : "Cart doesn't exist"}), HTTP_400_BAD_REQUEST
    
#     order = Orders(user_id=user_id, customer_id=customer_id, total_cost=0)
#     db.session.add(order)
#     db.session.commit()
    
#     return jsonify({'response' : "Order was successfully added",
#                     'order' : { 
#                         'order_id' : order.order_id,
#                         'user_id' : order.user_id,
#                         'customer_id' : order.customer_id,
#                         'total_cost' : order.total_cost
#                      }}), HTTP_200_OK


# @app.post('/api/order_detail')
# def api_order_detail():
    # cart = session.get('cart')
    # products_cost =[]
    # product_in_cart = {}
    # total_cost = 0
    # order_id = request.json['order_id']
    # order = Orders.query.get(order_id)

    # for item in cart:
    #     if cart == []:
    #         return jsonify({'error' : "Yours cart is empty"}), HTTP_404_NOT_FOUND
        
    #     product_id = int(item['product_id'])
    #     quantity = int(item['quantity'])
    #     product = Products.query.get(product_id)

    #     if product:
    #         total_product_cost = product.cost * quantity
    #         products_cost.append(total_product_cost)

    #         order_detail = Orders_detail(
    #                         order_id=order.order_id,
    #                         product_id=product_id,
    #                         quantity_of_product=quantity)
            
    #         db.session.add(order_detail)
    #         product_in_cart[product_id] = {
    #             'ilosc': quantity,
    #             'cena_za_produkt': product.cost,
    #             'suma': total_product_cost}
            

    # total_cost = sum(products_cost)
    # order.total_cost = total_cost
    # db.session.commit()
    

    # return jsonify({'response' : " Order_detail was succesfully added",
    #                 'order_detail' : { 
    #                     'order_id' :  order_detail.order_id,
    #                     'product_id' : order_detail.product_id,
    #                     'quantity_of_product' : order_detail.quantity_of_product,
    #                     'total_cost' : order.total_cost
    #                  }}), HTTP_200_OK

# TODO BEZ AJAXA ciezko ? 
# @app.post('/api/payment/<int:order_id>')
# def api_payment(order_id):
#     order_id = request.json['order_id']
#     order = Orders.query.get(order_id)
   
#     # Customer info, stripe token 4242 4242 4242 4242
#     customer = stripe.Customer.create(email =  request.json['stripeEmail'],
#                                       source = request.json['stripeToken'])
    
#     # Payment info
#     charge = stripe.Charge.create(
#         customer = customer.id,
#         amount=order.total_cost,
#         currency='usd',
#         description='Płatność'
#     )

#     return jsonify({'response' : "Payment was success",
#                     'total_cost' : charge.amount}), HTTP_200_OK

# @app.get('/api/summary')
# def api_summary():
#     cart = session.get('cart')
#     order_id = request.json['order_id']
#     order = Orders.query.get(order_id)

#     return jsonify({'response' : 'Order summary',
#                     'cart' : cart,
#                     'order' : { 
#                         'order_id' : order.order_id,
#                         'user_id' : order.user_id,
#                         'customer_id' : order.customer_id,
#                         'total_cost' : order.total_cost
#                      }}), HTTP_200_OK









# if __name__ == '__main__':
#     app.run(debug=True, port=5000)











''' 
SCHEMAT ZAKUPOWY

NORMALIZACJA

# user: 1, maciek12, Maciek, maciek@wp.pl, 2137
# user: 2, karol12, Karol, karol@wp.pl, 21372

# product: 1, karma, 12, whiskas, 213123
# product: 2, gowno, 121, dupa, 12312314


    #Maciek 12 zmienia nick:

    # 1. Jest tak ustawione zeby zmiana nicku integrowala baze danych i wszystkie Maciek12 zmienia sie na nowy nick
    # 2. Baza danych zostaje niezmieniona i wszystkie zakupy Maciek12 zostaja tak jak są nieruszone
    # 3. Jezeli pojawi sie nowy Maciek12 to i tak bedzie mial inny primary_key
    # 
    # 4. Czy można ustawić db zakupy żeby brały tylko primary key innych tabel ?
    # 4. Odpowiedź : ForeginKey do ustawiania rekordu (rzędu) w innej tabeli. "Column("user_id", Integer, ForeignKey("user.user_id"), nullable=False)"
    # Co jeśli maciek12 kupi więcej niż jeden produkt
    # n-n relation
    #  inne relacje (1-1 np. | 1-n jeden-do-wielu | n-n wiele do wielu | )

# zamówienie: id (pk), id_user (fk), data, kwota
# zamówienie: 1, 1, 13.01.1212, 11
# zamówienie: 2, 2, 13.12.2137, 20

# zamówienie_detal: id_zamówienie_detal (pk), zamówienie_id (fk), id_produkt (fk), ilosc
# zamówienie_detal: 1, 1, 1, 2
# zamówienie_detal: 2, 1, 2, 7
# zamówienie_detal: 3, 1, 3, 2
# zamówienie_detal: 4, 2, 1, 2
# zamówienie_detal: 5, 2, 2, 1

Robisz jakiś endpoint np /add-to-cart przyjmujący POST
Na stronie robisz JavaScript który wykonuje asynchroniczny request (tj. taki który nie przeładowuje strony) 
tzn. AJAX endpoint /add-to-cart dostaje sesje usera (czy to możliwe?), produkt oraz ilość i dodaje mu te dane 
do jego słownika sesji endpoint zwraca JSON z aktualnym koszykiem usera






Jeśli chce wiedzieć więcej to zobaczę

teoria
- normalizacja 
    - https://devszczepaniak.pl/postaci-normalne/
    - https://pl.wikipedia.org/wiki/Posta%C4%87_normalna_(bazy_danych)
- ACID - atomicity, consistency, isolation, durability
    - https://pl.wikipedia.org/wiki/ACID
- CAP theroem
    - https://en.wikipedia.org/wiki/CAP_theorem

praktyka
- sharding - rozłożenie baz danych na kilka pomniejszych
- indexy - do optymalizacji wyszukiwania w tabeli
- transakcje - Poznanie koncepcji transakcji i transakcyjności w bazach danych.
- WHERE i JOIN. + optymalizacja zapytań
'''


    #TODO LIST

    # czemu w panelu admina przy dodawaniu produktu nie ma dodawania do category id 
       
    # Entity schema (nazwy encji powinny byc w pojedynczej), ERD online(zapytac Adama w czym robił)
    
    # Po całej stronie zrobić api. Aplikacje, która bedzie zwracała czyste informacje, za pomocą flassgera np. z endpointami (JS etc)

    # ogarnąc żeby przy logowaniu nie było widac hasła gołym okiem w zbadaj źródło, payload (zoabczyc HTTPS co i jak, self certyfiakt 509)

    # dodać maxlength do inputow, ktore dotycza kolumn z ogranizczona liczba znakow

    # dodac walidacje danych otrzymywanych z frontu, zeby np. jako ilosc nie móc podać "aaaeee"

'''
Po zrobieniu api zrobić autoryzacje i token lata po froncie
'/auth -> [email, password] => token
token (id, roles: [ ] ) 
FE -> Authorization.header = Berearer <token>
'POST -> includes <token> -> decode -> roles.includes('admin)


'''

'''  


Folder "constants" (stałe) w aplikacji Flask może być używany do przechowywania stałych, które są używane w różnych częściach aplikacji. Jest to dobre praktyka, ponieważ pozwala to na scentralizowane zarządzanie stałymi i ułatwia zmiany w razie potrzeby.

W takim folderze możesz przechowywać różne rodzaje stałych, takie jak:

Stałe związane z konfiguracją aplikacji, takie jak nazwy baz danych, klucze API, adresy URL innych usług, itp.
Stałe związane z wiadomościami wyświetlanymi w interfejsie użytkownika, takie jak komunikaty o błędach, wiadomości sukcesu, teksty na przyciskach, itp.
Stałe związane z logiką biznesową, takie jak maksymalne długości pól formularza, wartości stałe wykorzystywane w obliczeniach, itp.
Przykładowa struktura folderu "constants" w aplikacji Flask mogłaby wyglądać tak:

arduino
Copy code
my_flask_app/
    app/
        constants/
            __init__.py
            config.py
            messages.py
            business_logic.py
        routes.py
        models.py
        templates/
        static/
    tests/
    config.py
    run.py
W pliku __init__.py w folderze "constants" możesz zdefiniować moduł jako pakiet, a następnie w poszczególnych plikach, takich jak config.py, messages.py, business_logic.py, przechowywać odpowiednie stałe w formie zmiennych lub klas.

Na przykład w pliku config.py możesz mieć:

python
Copy code
DEBUG = True
DATABASE_URI = 'sqlite:///mydatabase.db'
SECRET_KEY = 'super_secret_key'
W pliku messages.py możesz mieć:

python
Copy code
ERROR_MESSAGES = {
    'not_found': 'Nie znaleziono zasobu.',
    'unauthorized': 'Brak autoryzacji.'
}
W pliku business_logic.py możesz mieć:

python
Copy code
MAX_USERNAME_LENGTH = 50
MAX_PASSWORD_LENGTH = 100
Następnie możesz importować te stałe w innych częściach swojej aplikacji, takich jak pliki routingu, modele, itp., co pozwoli uniknąć duplikacji kodu i ułatwi zmiany w stałych, gdy zajdzie taka potrzeba.









'''


# DO BYKA
# jak ustawic zeby co odpalenie vscoda nie trzeba bylo pisacFLASK_ENV = 'development'FLASK_APP= 'src' FLASK_DEBUG=1, tylko zeby config wczytywał to tak jak powinien/ czemu nie wczytuje ? powinien byc ustawione export FLASK_ENV="development" i wszędzie przed kodem export ?

# jak ustawić word wrapa na stałe
# czemu w __init__ dwie funkcje są przyeciemnione 

# DO STAJKIEGO


# zawsze liczba mnoga w linkach w route a potem single rzecz po id /api/products     api/products/1
# JWT TOKENY
# DOCKER
# mcertyfikat SSL zeby po https lecialo
# content pod seo  jak powinien wygladac

"""

/api/product/ [ GET (localhost:5000/api/product?price_low=10&price_high=50) | POST | DELETE ] / filtrowanie produktów ?
- GET = pokaż produkty, możliwe filtrowanie
- POST = dodaj produkt
- DELETE = usuń produkty

"""

