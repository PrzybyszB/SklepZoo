from flask import Flask, render_template, flash, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
# from sites import sites
from datetime import datetime
from webforms import LoginForm, UserForm, PasswordForm, ProductForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user

app = Flask(__name__)

#Add Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db' 

#Secret Key!
app.config['SECRET_KEY'] = "test haslo" # uwazac zeby nie podawac  w gita bo wjedzie na publik i  bedzie iks de

# Initialize The Database
db = SQLAlchemy(app)


#Flask_Login Stuff
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

#TODO LOGOWANIE, INICIACJE DATABASE python3 app.app_context()

@app.route("/")
def home():
    return render_template("index.html")

#Create User add function
@app.route('/user/add', methods=['GET', 'POST'])
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
                         password_hash=hashed_pw)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.username.data = ''
        form.email.data = ''
        form.password_hash.data = ''
        flash("User Added Successfully")
    our_users = Users.query.order_by(Users.data_added)
    return render_template("add_user.html", 
                           form=form,
                           name=name,
                           our_users=our_users)

#Create Login function
@app.route("/login" ,methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user:
            #check the hash
            if check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                flash("Login successfull")
                return redirect(url_for('dashboard'))
            else:
                flash("Wrong password - Try again")
        else:
            flash("That user doeasn't exist")
    return render_template('login.html', form=form)

#Create Log out function
@app.route('/logout',methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash("U have been logged out!")
    return redirect(url_for('login'))

#Create Dashboard Page
@app.route('/dashboard',methods=['GET', 'POST'])
@login_required
def dashboard():
    form = UserForm()
    id = current_user.id
    name_to_update = Users.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.favorite_color = request.form['favorite_color']
        name_to_update.username = request.form['username']
        try:
            db.session.commit()
            flash("Users Updated Successfully")
            return render_template('dashboard.html',
                                   form=form,
                                   name_to_update = name_to_update)
        except:
            flash("Error ! Try again")
            return render_template('dashboard.html',
                                   form = form,
                                   name_to_update = name_to_update)
    else:
        return render_template('dashboard.html',
                                   form = form,
                                   name_to_update = name_to_update,
                                   id = id)

#Create Add Product Page
@app.route("/add_product" ,methods=['GET', 'POST'])
def add_product():
    product_name = None
    form = ProductForm()
    if form.validate_on_submit():
        product = Products.query.filter_by(email=form.email.data).first()
        if product is None:
            product = Products(product_name=form.product_name.data,
                         id = form.id.data, 
                         producent = form.producent.data,)
            db.session.add(product)
            db.session.commit()
        product_name = form.product_name.data
        form.product_name.data = ''
        form.id.data = ''
        form.cost.data = ''
        form.producent.data = ''
        form.data_added.data = ''
        flash("Product Added Successfully")
    our_products = Products.query.order_by(Products.data_added)
    return render_template('add_product.html', 
                           form=form,
                           product_name=product_name,
                           our_products=our_products)

    



@app.route('/products', methods=['GET', 'POST'])
def products():
    return render_template('products.html')


@app.route('/sucha_karma', methods=['GET', 'POST'])
def sucha_karma():
    return render_template('sucha_karma.html')


@app.route('/mokra_karma', methods=['GET', 'POST'])
def mokra_karma():
    return render_template('mokra_karma.html')


@app.route('/zabawki', methods=['GET', 'POST'])
def zabawki():
    return render_template('zabawki.html')



#DB MODELS

#Create Model
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    data_added = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Doing password stuff
    password_hash = db.Column(db.String(128))
    password_hash - db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError ('password is not readable attribute')
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    def verify_password(self,password):
        return check_password_hash(self.password_hash, password)
    # Create A String
    def __repr__(self):
        return '<Name %r>' % self.name

class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(200), nullable=False)
    cost = db.Column(db.Integer, primary_key=True)
    producent = db.Column(db.String(200), nullable=False)
    data_added = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Create A String
    def __repr__(self):
        return '<Name %r>' % self.name

if __name__ == '__main__':
    app.run(debug=True, port=5000)