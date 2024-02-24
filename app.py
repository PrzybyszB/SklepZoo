from flask import Flask, render_template, flash, request, redirect, url_for, session
from flask_migrate import Migrate
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
# import flask_login as login
from flask_admin import Admin, AdminIndexView, expose, helpers
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from webforms import LoginForm, UserForm, ProductForm, CategoryForm, Order_detailForm, CustomerForm
from werkzeug.security import generate_password_hash, check_password_hash
import re
import stripe


app = Flask(__name__)



#Add Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://pbartosz:1q2w3e4r5t6Y.@localhost/FirstDataBase'

#Secret Key!
app.config['SECRET_KEY'] = "test haslo" # uwazac zeby nie podawac  w gita bo wjedzie na publik i  bedzie iks de

# Initialize The Database
db = SQLAlchemy(app)

# Flask migrate instance
migrate = Migrate(app,db)

#DB MODELS

#Create Model
class Users(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    name = db.Column(db.String(200), nullable=False)
    last_name = db.Column(db.String(200), nullable=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    adress = db.Column(db.String(120), nullable=True)
    data_added = db.Column(db.DateTime, default=datetime.utcnow)
    orders_relationship = db.relationship('Orders', backref='users', lazy=True)


    # 
    @property
    def is_authenticated(self):
        return True
    
    @property
    def is_active(self):
        return True
    

    @property
    def is_anonymous(self):
        return False
    
    # Doing changes about user_id define, default is define as id in login stuff
    def get_id(self):
        return (self.user_id)
    
    @property
    def is_anonymous(self):
        return False


    # Resolve : sqlalchemy.exc.InvalidRequestError: Entity namespace for "users" has no property "id"
    @property
    def id(self):
        return self.user_id
    
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

class Category(db.Model):
    category_id = db.Column(db.Integer, primary_key=True, index=True)
    category_name =db.Column(db.String(50), unique=True, nullable=False)
    products_relationship = db.relationship('Products', backref='category', lazy=True)

class Products(db.Model):
    product_id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(200), nullable=False)
    cost = db.Column(db.Integer, nullable=True)
    producent = db.Column(db.String(200), nullable=False)
    data_added = db.Column(db.DateTime, default=datetime.utcnow)
    category_id = db.Column(db.Integer, db.ForeignKey('category.category_id'), nullable=False,)
    order_detail_relationship = db.relationship('Orders_detail', backref='products', lazy=True)

class Orders(db.Model):
    order_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True,)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id'), nullable=True,)
    order_data = db.Column(db.DateTime, default=datetime.utcnow)
    total_cost = db.Column(db.Integer, nullable=False)
    order_detail_relationship = db.relationship('Orders_detail', backref='orders', lazy=True)

class Orders_detail(db.Model):
    order_detail_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id'), nullable=True,)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), nullable=True)
    quantity_of_product = db.Column(db.Integer, nullable=False)
    
class Customer(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=True, unique=True)
    name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    adress = db.Column(db.String(120), nullable=False)
    order_detail_relationship = db.relationship('Orders', backref='customer', lazy=True)

'''
TODO https://flask-admin.readthedocs.io/en/latest/introduction/#rolling-your-own
https://github.com/flask-admin/Flask-Admin/tree/master/examples/auth-flask-login.
zobaczyc ten kod źródłowy jak połączyć login flask i flask admin
'''
# Flask admin view, username = Admin, password = 123, email = Admin@email.com, user_id = 1
class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if current_user.is_authenticated:
            id = current_user.user_id
            if id == 1:
              return super(MyAdminIndexView, self).index()  
        if not current_user.is_authenticated:
            flash('U have to be Admin to do Admin things')
            return redirect(url_for('login'))
        else:
            flash('U have to be Admin to do Admin things')
            return redirect(url_for('dashboard'))


# Flask admin init base_template='admin.html')
        
admin = Admin(app, name='Admin',index_view=MyAdminIndexView(), template_mode='bootstrap3')

admin.add_view(ModelView(Products, db.session))
admin.add_view(ModelView(Category, db.session))
admin.add_view(ModelView(Users, db.session))

#Flask_Login Stuff
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


# For payments
public_key = "pk_test_TYooMQauvdEDq54NiTphI7jx"
stripe.api_key = "sk_test_4eC39HqLyjWDarjtT1zdp7dc"



@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template("index.html")

# Making session time 24h
@app.before_request
def make_session_time():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=1440)


#Create User add function
@app.route('/user_add', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
    print(form.errors)
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            # Hash password
            hashed_pw = generate_password_hash(form.password_hash.data, "pbkdf2:sha256")
            user = Users(name=form.name.data,
                         username = form.username.data, 
                         email = form.email.data, 
                         password_hash=hashed_pw,
                         adress = None,
                         last_name = None)
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
    id = current_user.user_id
    name_to_update = Users.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
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


@app.route('/add_category' ,methods=['GET', 'POST'])
@login_required
def add_category():
    id = current_user.user_id
    if id == 1:
        category_name = None
        form = CategoryForm()
        if form.validate_on_submit():
            check_exist_category =  Category.query.filter_by(category_name=form.category_name.data).first()
            if check_exist_category is None:
                new_category = Category(category_name = form.category_name.data)
                
                db.session.add(new_category)
                db.session.commit()
            category_name = form.category_name.data
            form.category_name.data = ''
            flash("Category Added Successfully")
        category_list = Category.query.order_by(Category.category_id)
        return render_template('add_category.html', 
                            form=form,
                            category_name = category_name,
                            category_list = category_list)
    else:
        flash("Ooops, something went wrong")
        return redirect(url_for('dashboard'))


@app.route('/add-product' ,methods=['GET', 'POST'])
@login_required
def add_product():
    id = current_user.user_id
    if id == 1:
        # category_id = Products.category_id
        product_name = None
        form = ProductForm()
        if form.validate_on_submit():
            product = Products.query.filter_by(product_name=form.product_name.data).first()
            if product is None:
                product = Products(product_name=form.product_name.data,
                                cost = form.cost.data,
                                    producent = form.producent.data,
                                    category_id = form.category_id.data)
                
                db.session.add(product)
                db.session.commit()
            product_name = form.product_name.data
            form.product_name.data = ''
            form.cost.data = ''
            form.producent.data = ''
            form.category_id.data = ''
            flash("Product Added Successfully")
        our_products = Products.query.order_by(Products.data_added)
        return render_template('add_product.html', 
                            form=form,
                            product_name=product_name,
                            our_products=our_products)
    else:
        flash("Ooops, something went wrong")
        return redirect(url_for('dashboard'))
    
@app.route('/products', methods=['GET', 'POST'])
def products():
    our_products = Products.query.order_by(Products.data_added)
    return render_template('products.html', 
                           our_products=our_products)


@app.route('/sucha_karma', methods=['GET', 'POST'])
def sucha_karma():
    dry_foods = Products.query.filter_by(category_id = 1 )
    return render_template('sucha_karma.html', 
                           dry_foods=dry_foods,)


@app.route('/mokra_karma', methods=['GET', 'POST'])
def mokra_karma():
    wet_foods = Products.query.filter_by(category_id = 2 )
    return render_template('mokra_karma.html', 
                           wet_foods=wet_foods,)


@app.route('/zabawki', methods=['GET', 'POST'])
def zabawki():
    toys = Products.query.filter_by(category_id = 3 )
    return render_template('zabawki.html', 
                           toys=toys,)


@app.route('/user-list', methods=['GET', 'POST'])
@login_required
def user_list():
    id = current_user.user_id
    if id == 1:
        our_users = Users.query.order_by(Users.email)
        return render_template('user_list.html',
                           our_users=our_users)
    else:
        flash("Ooops, something went wrong")
        return redirect(url_for('dashboard'))

@app.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(user_id):
    form = UserForm()
    name_to_update = Users.query.get_or_404(user_id)
    if request.method == "POST":
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.username = request.form['username']
        try:
            db.session.commit()
            flash("Users Updated Successfully")
            return render_template('update.html',
                                   form=form,
                                   name_to_update = name_to_update)
        except:
            flash("Error ! Try again")
            return render_template('update.html',
                                   form = form,
                                   name_to_update = name_to_update)
    else:
        return render_template('update.html',
                                   form = form,
                                   name_to_update = name_to_update,
                                   user_id = user_id)


@app.route('/cart', methods=['GET', 'POST'])
def cart():
    form = Order_detailForm()
    cart = session.get('cart', [])
    
    return render_template("cart.html", cart=cart, form=form)


@app.route('/update_cart', methods=['GET', 'POST'])
def update_cart():    
    if request.method == "POST":
        cart = session.get('cart', [])

        # Creating group using regex to sort our cart
        pattern = re.compile(r"items\[(\d+)\]\[(quantity|product_id)\]")
        cart_list = {}
        for key in request.form.keys():
            match = pattern.match(key)
            if match:
                index = int(match.group(1))
                if index not in cart_list:
                    cart_list[index] = {}
                cart_list[index][match.group(2)] = ((key, request.form[key]))
        
        # Extract quantity of product from cart and change a value to quantity from sorting request.form
        for index, product_details_items in sorted(cart_list.items(), key=lambda x: int(x[0])):
            product_details = [product_details_items['quantity'], product_details_items['product_id']]
            for quantity in product_details:
                quantity = int(product_details_items['quantity'][1])
                if quantity != cart[int(index)]['quantity']:
                    cart[int(index)]['quantity'] = quantity
        
        #Saving up to date cart in session
        session['cart'] = cart
        session.modified = True
        return redirect(url_for('cart'))
    else:
        return redirect(url_for('cart'))


@app.route('/product/<int:product_id>', methods=['GET', 'POST'])
def product(product_id):
    form1 = ProductForm()
    form2 = Order_detailForm()
    product = Products.query.get_or_404(product_id)
    # product = Products(product_id=product_id, product_name='Produkt1', cost=11, producent="Producent1", category_id=1)
    
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
        return redirect(url_for("cart"))
    else:
        return render_template('product.html', 
                               product=product, 
                               form2=form2, 
                               form1=form1,)


@app.route('/order', methods=["GET","POST"])
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
            return redirect(url_for("orders_detail", user_email=user_email))
        elif customer_form.validate_on_submit():
            customer_user = Customer(email = customer_form.email.data,
                                  name = customer_form.name.data,
                                  last_name = customer_form.last_name.data,
                                  adress = customer_form.adress.data)
            db.session.add(customer_user)
            db.session.commit()
            user_email = customer_form.email.data
            return redirect(url_for("orders_detail", 
                    user_email = user_email,))
    return render_template('order.html', 
                           cart = cart, 
                           user_form = user_form, 
                           customer_form = customer_form)


@app.route('/orders_detail/<user_email>', methods=["GET", "POST"])
def orders_detail(user_email):
    form = UserForm(request.form)
    cart = session.get('cart')
    products_cost =[]
    product_in_cart = {}
    total_cost = 0
    customer = Customer.query.filter_by(email = user_email).first()
    user = Users.query.filter_by(email = user_email).first()
    
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
        product = Products.query.get(product_id)

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
            print(product_in_cart)

    total_cost = sum(products_cost)
    order.total_cost = total_cost
    db.session.commit()
    
    return render_template("orders_detail.html",
                           form=form,
                           cart=cart,
                           user_email=user_email,
                           order_id=order.order_id)


@app.route('/summary/<int:order_id>', methods=["GET", "POST"])
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
    

@app.route('/payment/<int:order_id>', methods=["GET","POST"])
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

    return redirect(url_for('final_order_info'))


@app.route('/final_order_info', methods=["GET","POST"])
def final_order_info():
    return render_template('final_order_info.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)











''' 
SCHEMAT ZAKUPOWY

NORMALIZACJA

# user: 1, maciek12, Maciek, maciek@wp.pl, 2137
# user: 2, karol12, Karol, karol@wp.pl, 21372

# product: 1, karma, 12, whiskas, 213123
# product: 2, gowno, 121, dupa, 12312314


    #Maciek 12 zmienia nick:

    # 1. Jest tak ustawione zeby zmiana nicku integrowala baze danych i wszystkie Maciek12 zmienia sie na nowy nick
    # 2. Baza danych zostaje niezmieniona i wszystkie zakupy Maciek12 zostaja tak jak są nieruszone
    # 3. Jezeli pojawi sie nowy Maciek12 to i tak bedzie mial inny primary_key
    # 
    # 4. Czy można ustawić db zakupy żeby brały tylko primary key innych tabel ?
    # 4. Odpowiedź : ForeginKey do ustawiania rekordu (rzędu) w innej tabeli. "Column("user_id", Integer, ForeignKey("user.user_id"), nullable=False)"
    # Co jeśli maciek12 kupi więcej niż jeden produkt
    # n-n relation
    #  inne relacje (1-1 np. | 1-n jeden-do-wielu | n-n wiele do wielu | )

# zamówienie: id (pk), id_user (fk), data, kwota
# zamówienie: 1, 1, 13.01.1212, 11
# zamówienie: 2, 2, 13.12.2137, 20

# zamówienie_detal: id_zamówienie_detal (pk), zamówienie_id (fk), id_produkt (fk), ilosc
# zamówienie_detal: 1, 1, 1, 2
# zamówienie_detal: 2, 1, 2, 7
# zamówienie_detal: 3, 1, 3, 2
# zamówienie_detal: 4, 2, 1, 2
# zamówienie_detal: 5, 2, 2, 1

Robisz jakiś endpoint np /add-to-cart przyjmujący POST
Na stronie robisz JavaScript który wykonuje asynchroniczny request (tj. taki który nie przeładowuje strony) 
tzn. AJAX endpoint /add-to-cart dostaje sesje usera (czy to możliwe?), produkt oraz ilość i dodaje mu te dane 
do jego słownika sesji endpoint zwraca JSON z aktualnym koszykiem usera






Jeśli chce wiedzieć więcej to zobaczę

teoria
- normalizacja 
    - https://devszczepaniak.pl/postaci-normalne/
    - https://pl.wikipedia.org/wiki/Posta%C4%87_normalna_(bazy_danych)
- ACID - atomicity, consistency, isolation, durability
    - https://pl.wikipedia.org/wiki/ACID
- CAP theroem
    - https://en.wikipedia.org/wiki/CAP_theorem

praktyka
- sharding - rozłożenie baz danych na kilka pomniejszych
- indexy - do optymalizacji wyszukiwania w tabeli
- transakcje - Poznanie koncepcji transakcji i transakcyjności w bazach danych.
- WHERE i JOIN. + optymalizacja zapytań
'''


    #TODO LIST


    # Ogarnąć żeby na stronie orders_detail zapisywało do db Orderdateail gdy będzie opłacone
    
    # Zrobić w panelu Admina, żeby home cofało do strony głównej strony a nie panelu

    # BACKUP bazy danych zrobić (skopiować sobie po zrobieniu bazy userów i produktów) 
    
    # Kiedy dodajemy kategorie niech, dodaje sie automatycznie do SelectField i do navbaru
       
    # Entity schema (nazwy encji powinny byc w pojedynczej), ERD online(zapytac Adama w czym robił)
    
    # Po całej stronie zrobić api. Aplikacje, która bedzie zwracała czyste informacje, za pomocą flassgera np. z endpointami (JS etc)



'''
Po zrobieniu api zrobić autoryzacje i token lata po froncie
'/auth -> [email, password] => token
token (id, roles: [ ] ) 
FE -> Authorization.header = Berearer <token>
'POST -> includes <token> -> decode -> roles.includes('admin)


'''




# DO BYKA

# JWT TOKENY
# DOCKER
# mcertyfikat SSL zeby po https lecialo
# content pod seo  jak powinien wygladac