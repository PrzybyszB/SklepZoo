from flask import Blueprint, render_template
from src.db_models import Category

views_blueprint = Blueprint('views_blueprint', __name__, static_folder="static", template_folder="templates" )


@views_blueprint.route("/", methods=['GET', 'POST'])
def home():
    return render_template("index.html")
