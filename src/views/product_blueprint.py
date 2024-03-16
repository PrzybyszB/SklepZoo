from flask import Flask, Blueprint, render_template, flash, request, redirect, url_for, session, jsonify
from flask_login import login_required, current_user
from db_models import db, Products, Category
from webforms import ProductForm, CategoryForm, Order_detailForm




product_blueprint = Blueprint('product_blueprint', __name__, static_folder="static", template_folder="templates")



@product_blueprint.route('/add_category' ,methods=['GET', 'POST'])
@login_required
def add_category():
    id = current_user.user_id
    if id == 1:
        category_name = None
        form = CategoryForm()
        if form.validate_on_submit():
            check_exist_category =  Category.query.filter_by(category_name=form.category_name.data).first()
            if check_exist_category is None:
                new_category = Category(category_name = form.category_name.data,
                                        category_slug = form.category_slug.data)
                
                db.session.add(new_category)
                db.session.commit()
            category_name = form.category_name.data
            form.category_name.data = ''
            form.category_slug.data = ''
            flash("Category Added Successfully")
        category_list = Category.query.order_by(Category.category_id)
        return render_template('add_category.html', 
                            form=form,
                            category_name = category_name,
                            category_list = category_list)
    else:
        flash("Ooops, something went wrong")
        return redirect(url_for('user_blueprint.dashboard'))


@product_blueprint.route('/category/<category_slug>' ,methods=['GET', 'POST'])
def category(category_slug):
    category = Category.query.filter_by(category_slug = category_slug).first()
    category_list = Products.query.filter_by(category_id = category.category_id, deleted_at=None )
    category_name = category.category_name
    
    return render_template('category.html', 
                           category_list=category_list,
                           category_name = category_name)

@product_blueprint.route('/add-product' ,methods=['GET', 'POST'])
@login_required
def add_product():
    id = current_user.user_id
    if id == 1:
        # category_id = Products.category_id
        product_name = None
        form = ProductForm()
        if form.validate_on_submit():
            product = Products.query.filter_by(product_name=form.product_name.data, deleted_at=None).first()
            if product is None:
                product = Products(product_name=form.product_name.data,
                                cost = form.cost.data,
                                    producer = form.producer.data,
                                    category_id = form.category_id.data)
                
                db.session.add(product)
                db.session.commit()
            product_name = form.product_name.data
            form.product_name.data = ''
            form.cost.data = ''
            form.producer.data = ''
            form.category_id.data = ''
            flash("Product Added Successfully")
        our_products = Products.query.filter(Products.deleted_at == None).order_by(Products.data_added)
        return render_template('add_product.html', 
                            form=form,
                            product_name=product_name,
                            our_products=our_products)
    else:
        flash("Ooops, something went wrong")
        return redirect(url_for('user_blueprint.dashboard'))


@product_blueprint.route('/products', methods=['GET', 'POST'])
def products():
    our_products = Products.query.filter(Products.deleted_at == None).order_by(Products.data_added)
    return render_template('products.html', 
                           our_products=our_products)


@product_blueprint.route('/product/<int:product_id>', methods=['GET', 'POST'])
def product(product_id):
    form1 = ProductForm()
    form2 = Order_detailForm()
    product = Products.query.get_or_404(product_id)
    # product = Products(product_id=product_id, product_name='Produkt1', cost=11, producer="producer1", category_id=1)
    
    if request.method == "POST":
        quantity = int(request.form.get('quantity_of_product'))
        
        # If session['cart] exist, u download variable. If "cart" doeas not exist in the session, u create empty list "
        cart = session.get('cart', [])
        # This line checkout, if cart is dict. If yes, it convert into list(key,value)
        if isinstance(cart, dict):
            cart = list(cart.values())
        update = False
        for item in cart:
            if item['product_id'] == product.product_id:
                item['quantity'] += quantity
                update = True
                break
        if not update:
            cart.append({'product_id': product.product_id, 'quantity': quantity})
        session['cart'] = cart
        return redirect(url_for("cart_blueprint.cart"))
    else:
        return render_template('product.html', 
                               product=product, 
                               form2=form2, 
                               form1=form1,)

