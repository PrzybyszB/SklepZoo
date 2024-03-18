from flask import Blueprint, request, session, jsonify
from flasgger import swag_from
from src.db_models import Products
from src.constant.https_status_code import HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_404_NOT_FOUND






api_cart_blueprint = Blueprint('api_cart_blueprint', __name__, static_folder="static", template_folder="templates")


@api_cart_blueprint.get('/api/cart')
def api_cart():
    cart = session.get('cart', [])
    return jsonify({'cart' : cart}), HTTP_200_OK


@api_cart_blueprint.post('/api/cart')
def api_add_to_cart():
    cart = session.get('cart', [])
    if 'products' in request.json and isinstance(request.json['products'], list):
            for product in request.json['products']:
                product_id = product.get('product_id')
                quantity = product.get('quantity')
                product = Products.query.get(product_id)
                if product:
                    cart.append({'product_id': product_id, 'quantity': quantity})
                else:
                    return jsonify({'error' : f'Product with id {product_id} was not found',
                                    'cart' : cart}), HTTP_404_NOT_FOUND     
    session['cart'] = cart
        
    return jsonify({
        'respone' : "Products was added successfully",
        'cart': cart}), HTTP_200_OK
'''
{
    "products": [
        {
            "product_id": "2",
            "quantity": "3"
        },
        {
            "product_id": "4",
            "quantity": "1"
        }
    ]
}
'''


@api_cart_blueprint.route('/api/cart', methods = ['PUT'])
def api_update_cart():
    cart = session.get('cart', [])
    # If request is a list (more than one product)
    if isinstance(request.json, list):
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

