from flask import Flask, Blueprint, render_template, flash, request, redirect, url_for, session, jsonify
import stripe
from db_models import Orders





payment_blueprint = Blueprint('payment_blueprint', __name__, static_folder="static", template_folder="templates")


@payment_blueprint.route('/payment/<int:order_id>', methods=["GET","POST"])
def payment(order_id):
    order = Orders.query.get_or_404(order_id)
    # Customer info
    customer = stripe.Customer.create(email =  request.form['stripeEmail'],
                                      source = request.form['stripeToken'])
    
    # Payment info
    charge = stripe.Charge.create(
        customer = customer.id,
        amount=order.total_cost,
        currency='usd',
        description='Płatność'
    )

    return redirect(url_for('cart_blueprint.final_order_info'))