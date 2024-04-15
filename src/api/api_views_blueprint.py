from flask import Blueprint, request, session, jsonify
from flask_login import current_user
from flasgger import swag_from
from src.constant.https_status_code import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_200_OK
from src.db_models import db, Customer, Orders, Orders_detail, Products
from src.webforms import SearchForm
import validators




api_views_blueprint= Blueprint('api_views_blueprint', __name__, static_folder="static", template_folder="templates")

@swag_from('/src/docs/swag_views/api_home.yml')
@api_views_blueprint.get('/apihome')
def api_home():
    return jsonify({"response" : "This is home page"})


@api_views_blueprint.post('/api/customer_creator')
def api_customer_creator():
    
    if not current_user.is_authenticated:
        # Extract customer information from request JSON.
        name = request.json['name']
        last_name = request.json['last_name']
        email = request.json['email']
        address = request.json['address']

        if not validators.email(email):
            return jsonify({'error': "Email is not valid"}), HTTP_400_BAD_REQUEST

        customer_user = Customer(name = name,
                                 last_name = last_name,
                                 email = email,
                                 address = address)
        db.session.add(customer_user)
        db.session.commit()
        return jsonify({'respone' : 'customer was created',
                        'customer' : {
                            'name' : customer_user.name,
                            'last_name' : customer_user.last_name,
                            'email' : customer_user.email,
                            'address' : customer_user.address
                        }})
    return jsonify({'error' : "You cant create a customer when u are log in"}), HTTP_400_BAD_REQUEST


@api_views_blueprint.post('/api/order')
def api_order():
    # Initialize user_id and customer_id variables.
    user_id = None
    customer_id = None

    if current_user.is_authenticated:
        user_id = current_user.user_id

    else:
        customer_id = request.json['customer_id']

        # Check if the customer exists in the database
        customer = Customer.query.get(customer_id)

        # Check if the cart is empty
        if customer is None:
            return jsonify({'error' : "That customer doesn't exist"}), HTTP_400_BAD_REQUEST
    
    cart = session.get('cart')
    if cart is None:
        return jsonify({'error' : "Your cart is empty"}), HTTP_200_OK
    
    # Check if the cart exists but is not initialized properly
    if cart is not cart:
        return jsonify({'error' : "Cart doesn't exist"}), HTTP_400_BAD_REQUEST
    
    order = Orders(user_id=user_id, customer_id=customer_id, total_cost=0)
    db.session.add(order)
    db.session.commit()
    
    return jsonify({'response' : "Order was successfully added",
                    'order' : { 
                        'order_id' : order.order_id,
                        'user_id' : order.user_id,
                        'customer_id' : order.customer_id,
                        'total_cost' : order.total_cost
                     }}), HTTP_200_OK


@api_views_blueprint.post('/api/order_detail')
def api_order_detail():
    cart = session.get('cart')

    products_cost =[]
    product_in_cart = {}
    total_cost = 0

    # Retrieve order_id from request JSON
    order_id = request.json['order_id']

    # Get the order from the database
    order = Orders.query.get(order_id)

    for item in cart:
        if cart == []:
            return jsonify({'error' : "Yours cart is empty"}), HTTP_404_NOT_FOUND
        
        product_id = int(item['product_id'])
        quantity = int(item['quantity'])
        product = Products.query.get(product_id)
        
        # If the product exists, calculate the total cost for the product and update order details
        if product:
            total_product_cost = product.cost * quantity
            products_cost.append(total_product_cost)

            order_detail = Orders_detail(
                            order_id=order.order_id,
                            product_id=product_id,
                            quantity_of_product=quantity)
            
            db.session.add(order_detail)

            # Store product details in a dictionary for response
            product_in_cart[product_id] = {
                'ilosc': quantity,
                'cena_za_produkt': product.cost,
                'suma': total_product_cost}
            
    # Calculate total cost of the order
    total_cost = sum(products_cost)
    order.total_cost = total_cost
    db.session.commit()
    

    return jsonify({'response' : " Order_detail was succesfully added",
                    'order_detail' : { 
                        'order_id' :  order_detail.order_id,
                        'product_id' : order_detail.product_id,
                        'quantity_of_product' : order_detail.quantity_of_product,
                        'total_cost' : order.total_cost
                     }}), HTTP_200_OK


@api_views_blueprint.get('/api/summary')
def api_summary():
    
    cart = session.get('cart')
    order_id = request.json['order_id']
    order = Orders.query.get(order_id)

    return jsonify({'response' : 'Order summary',
                    'cart' : cart,
                    'order' : { 
                        'order_id' : order.order_id,
                        'user_id' : order.user_id,
                        'customer_id' : order.customer_id,
                        'total_cost' : order.total_cost
                     }}), HTTP_200_OK

