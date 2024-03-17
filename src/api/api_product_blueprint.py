from flask import Blueprint, request, jsonify
from flask_login import current_user
from src.db_models import db, Products, Category
from src.constant.https_status_code import HTTP_409_CONFLICT, HTTP_201_CREATED, HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND
from datetime import datetime





api_product_blueprint = Blueprint('api_product_blueprint', __name__, static_folder="static", template_folder="templates")


@api_product_blueprint.post('/api/category')
def api_add_category():
    if not current_user.is_authenticated:
        return jsonify({'error' : "Oops u are not login as Admin"}), HTTP_401_UNAUTHORIZED 
    
    if current_user.is_authenticated:
        id = current_user.user_id
        if id == 1:
            category_name = request.json['category_name']
            category_slug = request.json['category_slug']
            check_exist_category =  Category.query.filter_by(category_name=category_name).first()
            if check_exist_category is None:
                new_category = Category(category_name = category_name,
                                        category_slug = category_slug)
                db.session.add(new_category)
                db.session.commit()
                return jsonify({
                    'message': 'Category created',
                    'category_name' : category_name,
                    'category_slug' : category_slug
                }),  HTTP_201_CREATED
            else:
                return jsonify({'error' : " This category is already exist"}), HTTP_409_CONFLICT 
        else:
            return jsonify({'error' : "You are not Admin"}), HTTP_401_UNAUTHORIZED 


@api_product_blueprint.delete('/api/category')
def api_delete_category():
    if not current_user.is_authenticated:
        return jsonify({'error' : "Oops u are not login as Admin"}), HTTP_401_UNAUTHORIZED 

    if current_user.is_authenticated:
        id = current_user.user_id
        if id == 1:
            category_id = request.json['category_id']
            category_to_delete = Category.query.get(category_id)
            if category_to_delete is None:
                return jsonify({'error' : f'This category with ID: {category_id} does not exist'})
            db.session.delete(category_to_delete)
            db.session.commit()

            return jsonify({'response' : "Category was deleted"}), HTTP_200_OK
        else:
            return jsonify({'error' : "You are not Admin"}), HTTP_401_UNAUTHORIZED 
    

@api_product_blueprint.get('/api/category')
def api_category_list():
    our_categories = Category.query.order_by(Category.category_id).all()
    category_list = []

    for our_category in our_categories:
        category_name = our_category.category_name
        category_slug = our_category.category_slug
        category_id = our_category.category_id
        category_list.append({
                    "category_name" : category_name,
                    "category_slug" : category_slug,
                    "category_id" : category_id})
    return jsonify({"category_list" : category_list}), HTTP_200_OK


@api_product_blueprint.post('/api/product')
def api_add_product():
    if not current_user.is_authenticated:
        return jsonify({'error' : "Oops u are not login as Admin"}), HTTP_401_UNAUTHORIZED 

    if current_user.is_authenticated:
        id = current_user.user_id
        if id == 1:
            product_name = request.json['product_name']
            cost = request.json['cost']
            producer = request.json['producer']
            category_id = request.json['category_id']
            
            if Category.query.filter_by(category_id=category_id).first() is None:
                return jsonify({'error': "This category doesn't exist"}), HTTP_409_CONFLICT
            
            check_exist_product = Products.query.filter_by(product_name=product_name, deleted_at=None).first()
            if check_exist_product is None:
                new_product = Products(product_name=product_name,
                                        cost = cost,
                                        producer = producer,
                                        category_id = category_id)
                db.session.add(new_product)
                db.session.commit()
                return jsonify({
                    'message': 'Product added',
                    'product' : {
                                "product name" : product_name,
                                "cost" : cost,
                                "producer" : producer,
                                "category id" : category_id
                    }
                }),  HTTP_201_CREATED
        else:
            return jsonify({'error' : "You are not Admin"}), HTTP_401_UNAUTHORIZED 


@api_product_blueprint.delete('/api/product')
def api_delete_product():
    if not current_user.is_authenticated:
        return jsonify({'error' : "Oops u are not login as Admin"}), HTTP_401_UNAUTHORIZED 

    if current_user.is_authenticated:
        id = current_user.user_id
        if id == 1:
            product_id = request.json['product_id']
            product_to_delete = Products.query.filter_by(id=product_id, deleted_at=None).first()
            if product_to_delete is None:
                return jsonify({'error' : f'This product with ID: {product_id} does not exist'})
            product_to_delete.deleted_at = datetime.utcnow()
            db.session.commit()

            return jsonify({'response' : "Product was deleted"}), HTTP_200_OK
        else:
            return jsonify({'error' : "You are not Admin"}), HTTP_401_UNAUTHORIZED 


@api_product_blueprint.get('/api/product-list')
def api_products():
    our_products = Products.query.filter(Products.deleted_at == None).order_by(Products.data_added).all()
    product_list = []
    
    for our_product in our_products:
                product_name = our_product.product_name
                cost = our_product.cost
                producer = our_product.producer
                category_id = our_product.category_id

                product_list.append({
                    "product_name" : product_name,
                    "cost" : cost,
                    "producer" : producer,
                    "category_id" : category_id})
    
    return jsonify({"product_list" : product_list}), HTTP_200_OK


@api_product_blueprint.get('/api/product')
def api_product():
    product_id = request.json['product_id']
    product = Products.query.filter_by(product_id = product_id, deleted_at=None).first()
    if product is None:
        return jsonify({ 'error' : f'There is no product on product id {product_id}'}), HTTP_404_NOT_FOUND 
    else:
        return jsonify({
                    'product info': {
                        'product id' : product.product_id,
                        'product name': product.product_name, 
                        'cost' : product.cost,
                        'producer' : product.producer,
                        'category id' : product.category_id,
                        'data added' : product.data_added.strftime("%Y-%m-%d %H:%M:%S")
                    }}), HTTP_200_OK
    
