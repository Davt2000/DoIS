import json
from flask import render_template, request, current_app, session
from flask import Blueprint
from utilities.usedatabase import UseDatabase

query_routing = Blueprint('query_routing', __name__, template_folder='templates')


@query_routing.route('/', methods=['GET', 'POST'])
def query_():
    return render_template("../queries/templates/menu_query.html")