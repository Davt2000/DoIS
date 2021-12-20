from flask import Flask, render_template, session
import json
from users.log_session import auth_blueprint
from queries.query_handlers import query_handlers_blueprint
from queries.routes import query_routing_blueprint
from grid_editor.grid_editor import grid_editor_blueprint
from cart.cart_handler import cart_blueprint

app = Flask(__name__)

app.register_blueprint(query_routing_blueprint, url_prefix='/menu')
app.register_blueprint(query_handlers_blueprint, url_prefix='/queries')
app.register_blueprint(auth_blueprint, url_prefix='/login')
app.register_blueprint(grid_editor_blueprint, url_prefix='/editor')
app.register_blueprint(cart_blueprint, url_prefix='/marketplace')


with open('data/secret_key.json', 'r') as f:
    app.secret_key = json.load(f)['secret_key']


@app.route('/')
def index():
    if 'user' in session:
        rol = session['role']
        usr = session['user']
    else:
        rol = 'Unauthorized'
        usr = 'user'
    return render_template("index.html", rol=rol, usr=usr)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=True)
