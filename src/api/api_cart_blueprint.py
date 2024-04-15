from flask import Blueprint, request, session, jsonify
from flasgger import swag_from
from src.db_models import Products
from src.constant.https_status_code import HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_404_NOT_FOUND






api_cart_blueprint = Blueprint('api_cart_blueprint', __name__, static_folder="static", template_folder="templates")


@api_cart_blueprint.get('/api/cart')
@swag_from('/src/docs/swag_cart/api_cart.yml')
def api_cart():
    cart = session.get('cart', [])
    return jsonify({'cart' : cart}), HTTP_200_OK


@api_cart_blueprint.post('/api/cart')
@swag_from('/src/docs/swag_cart/api_add_to_cart.yml')
def api_add_to_cart():
    cart = session.get('cart', [])
    if 'products' not in request.json or not isinstance(request.json['products'], list):
        return jsonify({'error' : "Missing or invalid data" }), HTTP_400_BAD_REQUEST
    
    for product in request.json['products']:
        product_id = product.get('product_id')
        quantity = product.get('quantity')
        
        try:
            quantity = int(quantity)
        except ValueError:
            return jsonify({'error' : 'The quantity of product has to be integer'}), HTTP_400_BAD_REQUEST
        
        # Check if product_id and quantity are not empty.
        if product_id is None or quantity is None:
            return jsonify({'error' : "Missing or invalid data" }), HTTP_400_BAD_REQUEST
        
        existing_product = None
        # Check if the product already exists in the cart.
        for cart_product in cart:
            if cart_product['product_id'] == product_id:
                existing_product = cart_product
                break
        
        # If the product exists in the cart, update its quantity.
        if existing_product:
            existing_product['quantity']+= quantity
        else:
            # If the product doesn't exist in the cart, add it to the cart.
            product = Products.query.get(product_id)
            if not product:
                return jsonify({'error' : f'Product with id {product_id} was not found',
                                        'cart' : cart}), HTTP_404_NOT_FOUND 
        
            cart.append({'product_id': product_id, 'quantity': quantity})   
    
    session['cart'] = cart
        
    return jsonify({
            'respone' : "Products was added successfully",
            'cart': cart}), HTTP_200_OK


@api_cart_blueprint.route('/api/cart', methods = ['PUT'])
@swag_from('/src/docs/swag_cart/api_update_cart.yml')
def api_update_cart():
    cart = session.get('cart', [])

    # Check if the request JSON data is a list.
    if not isinstance(request.json, list):
        return jsonify({'error' : "Missing or invalid data" }), HTTP_400_BAD_REQUEST
    
    for item in request.json:
        if 'product_id' in item and 'quantity' in item:
            product_id = item['product_id']
            quantity = item['quantity']
            product_found = False

            for key in cart:
                if key['product_id'] == product_id:
                    key['quantity'] = quantity
                    product_found = True
                    
            if not product_found:
                return jsonify({'error': f'Product with ID: {product_id} was not found'}), HTTP_400_BAD_REQUEST
    
    session['cart'] = cart
    session.modified = True
    return jsonify({'message': 'Cart updated successfully', 'cart': cart}), HTTP_200_OK

