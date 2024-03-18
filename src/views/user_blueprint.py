from flask import Blueprint, render_template, flash, request, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from src.db_models import db, Users
from src.webforms import LoginForm, UserForm


user_blueprint = Blueprint('user_blueprint', __name__, static_folder="static", template_folder="templates")

@user_blueprint.route('/user_add', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            # Hash password
            hashed_pw = generate_password_hash(form.password_hash.data, "pbkdf2:sha256")
            user = Users(name=form.name.data,
                         username = form.username.data, 
                         email = form.email.data, 
                         password_hash=hashed_pw,
                         address = form.address.data,
                         last_name = form.last_name.data)
            
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.last_name.data = ''
        form.username.data = ''
        form.email.data = ''
        form.password_hash.data = ''
        form.address.data = ''
        flash("User Added Successfully")
    our_users = Users.query.order_by(Users.data_added)
    return render_template("add_user.html", 
                           form=form,
                           name=name,
                           our_users=our_users)


#Create Login function
@user_blueprint.route("/login" ,methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user:
            #check the hash
            if check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                flash("Login successfull")
                return redirect(url_for('user_blueprint.dashboard'))
            else:
                flash("Wrong password - Try again")
        else:
            flash("That user doeasn't exist")
    return render_template('login.html', form=form)


#Create Log out function
@user_blueprint.route('/logout',methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash("U have been logged out!")
    return redirect(url_for('user_blueprint.login'))


#Create Dashboard Page
@user_blueprint.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = UserForm()
    id = current_user.user_id
    user_to_update = Users.query.get_or_404(id)
    if request.method == "POST":
        user_to_update.name = request.form['name']
        user_to_update.last_name = request.form['last_name']
        user_to_update.username = request.form['username']
        user_to_update.address = request.form['address']
        try:
            db.session.commit()
            flash("Users Updated Successfully")
            return render_template('dashboard.html',
                                   form=form,
                                   user_to_update = user_to_update)
        except:
            flash("Error ! Try again")
            return render_template('dashboard.html',
                                   form = form,
                                   user_to_update = user_to_update)
    else:
        return render_template('dashboard.html',
                                   form = form,
                                   user_to_update = user_to_update,
                                   id = id)


@user_blueprint.route('/user-list', methods=['GET', 'POST'])
@login_required
def user_list():
    id = current_user.user_id
    if id == 1:
        our_users = Users.query.order_by(Users.email)
        return render_template('user_list.html',
                           our_users=our_users)
    else:
        flash("Ooops, something went wrong")
        return redirect(url_for('user_blueprint.dashboard'))


@user_blueprint.route('/update', methods=['GET', 'POST'])
@login_required
def update():
    form = UserForm()
    user_id = current_user.user_id
    user_to_update = Users.query.get_or_404(user_id)
    return render_template('update.html',
                                   form = form,
                                   user_to_update = user_to_update,
                                   user_id = user_id)
