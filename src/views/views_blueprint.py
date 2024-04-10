from flask import Blueprint, render_template
from src.webforms import SearchForm
from src.db_models import Products
views_blueprint = Blueprint('views_blueprint', __name__, static_folder="static", template_folder="templates" )


@views_blueprint.route("/", methods=['GET', 'POST'])
def home():
    return render_template("index.html")

@views_blueprint.route("/search", methods=["POST"])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        # Get data from submitted form
        product_searched = form.searched.data
        # Query the Database
        product = Products.query.filter(Products.deleted_at == None, Products.product_name.like('%' + product_searched + '%')).order_by(Products.product_name).all()

        return render_template("search.html", 
                               form=form, 
                               searched = product_searched,
                               product = product)