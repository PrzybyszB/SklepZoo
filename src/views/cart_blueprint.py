from flask import Flask, Blueprint, render_template, flash, request, redirect, url_for, session, jsonify
from flask_login import current_user
from src.webforms import  UserForm, Order_detailForm, CustomerForm
from src.db_models import db, Users, Products, Orders, Orders_detail, Customer
import re


cart_blueprint = Blueprint('cart_blueprint', __name__, static_folder="static", template_folder="templates")

# Public key for payment processing.
public_key = "pk_test_TYooMQauvdEDq54NiTphI7jx"

@cart_blueprint.route('/cart', methods=['GET', 'POST'])
def cart():
    form = Order_detailForm()
    cart = session.get('cart', [])
    
    return render_template("cart.html", cart=cart, form=form)


@cart_blueprint.route('/update_cart', methods=['GET', 'POST'])
def update_cart():    
    if request.method == "POST":
        cart = session.get('cart', [])

        # Creating group using regex to sort our cart.
        pattern = re.compile(r"items\[(\d+)\]\[(quantity|product_id)\]")
        cart_list = {}
        for key in request.form.keys():
            match = pattern.match(key)
            if match:
                index = int(match.group(1))
                if index not in cart_list:
                    cart_list[index] = {}
                cart_list[index][match.group(2)] = ((key, request.form[key]))
        
        # Extract quantity of product from cart and change a value to quantity from sorting request.form.
        for index, product_details_items in sorted(cart_list.items(), key=lambda x: int(x[0])):
            product_details = [product_details_items['quantity'], product_details_items['product_id']]
            for quantity in product_details:
                quantity = int(product_details_items['quantity'][1])
                if quantity != cart[int(index)]['quantity']:
                    cart[int(index)]['quantity'] = quantity
        
        # Saving up to date cart in session.
        session['cart'] = cart
        session.modified = True
        return redirect(url_for('cart_blueprint.cart'))
    else:
        return redirect(url_for('cart_blueprint.cart'))

@cart_blueprint.route('/order', methods=["GET","POST"])
def order():

    user_form = UserForm()
    customer_form = CustomerForm()
    cart = session.get('cart')
    user_email = None
    
    if request.method == "POST" or current_user.is_authenticated:
        if current_user.is_authenticated:
            user_email =  current_user.email
        else:
            user_email = None
        if user_email:
            return redirect(url_for("cart_blueprint.orders_detail", user_email=user_email))
        elif customer_form.validate_on_submit():
            # Create a new customer.
            customer_user = Customer(email = customer_form.email.data,
                                  name = customer_form.name.data,
                                  last_name = customer_form.last_name.data,
                                  address = customer_form.address.data)
            db.session.add(customer_user)
            db.session.commit()
            user_email = customer_form.email.data
            return redirect(url_for("cart_blueprint.orders_detail", 
                    user_email = user_email,))
    return render_template('order.html', 
                           cart = cart, 
                           user_form = user_form, 
                           customer_form = customer_form)


@cart_blueprint.route('/orders_detail/<user_email>', methods=["GET", "POST"])
def orders_detail(user_email):
    form = UserForm(request.form)
    cart = session.get('cart')
    products_cost =[]
    product_in_cart = {}
    total_cost = 0
    customer = Customer.query.filter_by(email = user_email).first()
    user = Users.query.filter_by(email = user_email).first()
    
    if cart == None:
        flash("Your cart is empty, choose products")
        return redirect(url_for('product_blueprint.products'))

    if user:
        user_id = user.user_id
        customer_id = None
    else:
        user_id = None
        customer_id = customer.customer_id

    order = Orders(user_id=user_id, customer_id=customer_id, total_cost=0)
    db.session.add(order)
    
    for item in cart:
        product_id = int(item['product_id'])
        quantity = int(item['quantity'])
        product = Products.query.filter_by(product_id=product_id, deleted_at=None).first()

        if product:
            total_product_cost = product.cost * quantity
            products_cost.append(total_product_cost)

            orders_detail = Orders_detail(
                            order_id=order.order_id,
                            product_id=product_id,
                            quantity_of_product=quantity)
            db.session.add(orders_detail)

            product_in_cart[product_id] = {
                'ilosc': quantity,
                'cena_za_produkt': product.cost,
                'suma': total_product_cost}
            

    total_cost = sum(products_cost)
    order.total_cost = total_cost
    db.session.commit()
    
    return render_template("orders_detail.html",
                           form=form,
                           cart=cart,
                           user_email=user_email,
                           order_id=order.order_id)


@cart_blueprint.route('/summary/<int:order_id>', methods=["GET", "POST"])
def summary(order_id):
    
    cart = session.get('cart')
    order = Orders.query.get_or_404(order_id)
    total_cost = order.total_cost
    orders_list = Orders.query.order_by(Orders.order_id)
    orders_detail_list = Orders_detail.query.all()
    return render_template("summary.html", order = order, 
                           total_cost = total_cost,
                           cart = cart,
                           orders_list = orders_list,
                           orders_detail_list = orders_detail_list,
                           public_key = public_key)
    
@cart_blueprint.route('/final_order_info', methods=["GET","POST"])
def final_order_info():
    return render_template('final_order_info.html')
