from flask import Flask, Blueprint, render_template, flash, request, redirect, url_for, session, jsonify
import stripe
from src.db_models import Orders
from src.constant.https_status_code import HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT, HTTP_201_CREATED, HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND,HTTP_500_INTERNAL_SERVER_ERROR






api_payment_blueprint = Blueprint('api_payment_blueprint', __name__, static_folder="static", template_folder="templates")


# TODO WIP payments.

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
