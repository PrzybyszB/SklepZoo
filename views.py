# from flask import Flask, Blueprint, render_template, flash, request, redirect, url_for
# from webforms import LoginForm, UserForm, PasswordForm
# from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
# from werkzeug.security import generate_password_hash, check_password_hash

# sites = Blueprint(__name__, "sites")

# @sites.route("/")
# def home():
#     return render_template("index.html")


# @sites.route("/login/<username>" ,methods=['GET', 'POST'])
# def Login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         user = Users.query.filter_by(username=form.username.data).first()
#         if user:
#             #check the hash
#             if check_password_hash(user.password_hash, form.password.data):
#                 login_user(user)
#                 flash("Login successfull")
#                 return redirect(url_for('dashboard'))
#             else:
#                 flash("Wrong password - Try again")
#         else:
#             flash("That user doeasn't exist")
#     return render_template('login.html', form=form)







