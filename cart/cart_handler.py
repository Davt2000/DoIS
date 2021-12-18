import json
from flask import request, current_app
from flask import Blueprint, session, render_template
from utilities.usedatabase import UseDatabase
from utilities.check_authority import in_session

cart_blueprint = Blueprint('cart_blueprint', __name__, template_folder='templates')


@cart_blueprint.route('/', methods=['GET', 'POST'])
@in_session
def start_handler():
    return


@cart_blueprint.route('/', methods=['GET', 'POST'])
@in_session
def session_handler():
    return


@cart_blueprint.route('/cart', methods=['GET', 'POST'])
@in_session
def cart_handler():
    with open('data/dbconfig.json', 'r', encoding='utf-8') as f:
        current_app.config['dbconfig'] = json.load(f)

    b_id = hash(session['user'])      # potentially unsafe

    if request.method == 'GET':
        cart = session.get('cart', None)

        if cart is None:
            cart = get_cart(b_id)
            if cart == ('emp',):
                cart = None         # ¯\_(ツ)_/¯
        else:
            save_cart(cart, b_id)
        return render_template('cart_base.html', items=cart, usr=session['user'])

    buy = request.form.get('buy')
    remove = request.form.get('del')
    drop = request.form.get('drop')

    if remove:
        session['cart'].pop(request.form.get('id_to_delete'))
    if drop:
        session['cart'] = dict()
        drop_cart(b_id)
    if buy:
        save_cart(session['cart'], b_id)
        buy_all(b_id)
        drop_cart(b_id)
    return render_template('cart_base.html', items=session['cart'], usr=session['user'])


def get_available_sessions():
    result = simple_sql(f"""
        SELECT F.Name, H.Name, Se.Data 
        FROM Session Se 
        JOIN Film F on F.F_id = Se.F_id  
        JOIN Hall H on H.H_id = Se.H_id
        WHERE Se.Data >= NOW()
    """)
    res = []
    schema = ['film', 'hall', 'datetime']
    for line in result:
        res.append(dict(zip(schema, line)))
    return res


def get_available_tickets(se_id):
    result = simple_sql(f"""
        SELECT T.T_id, T.Price, Sc.Row_ FROM Ticket T 
        JOIN Session Se on T.Se_id = Se.Se_id
        JOIN Scheme Sc on Sc.Sc_id = T.Sc_id
        WHERE Se.Se_id = {se_id}
        GROUP BY Sc.Row_, T.Price
    """)
    res = []
    schema = ['T_id', 'T_Price', 'row_']
    for line in result:
        res.append(dict(zip(schema, line)))
    return res


def get_cart(b_id):
    result = simple_sql(f"""
        SELECT T_id, F_name, T_price, B_item_id, B_paid FROM Basket
        WHERE B_id_hashed = {b_id}
    """)
    res = dict()
    schema = ['T_id', 'F_name', 'T_price', 'B_item_id', 'B_paid']
    for line in result:
        res[line[0]] = dict(zip(schema, line))
    return res


def update_cart():
    return


def drop_cart(b_id):
    simple_sql(f"""
    DELETE FROM Basket WHERE B_id_hashed = {b_id}
    """)
    return


def save_cart(cart_content, b_id):
    drop_cart(b_id)
    for it_ in cart_content:
        simple_sql(f"""
            INSERT INTO Basket (B_id_hashed, F_name, T_price, T_id, B_paid)
            VALUES ({b_id}, {it_["F_name"]}, {it_["T_price"]}, {it_["T_id"]}, 0) 
        """)
    return


def buy_all(b_id):
    result = simple_sql(f"""
            SELECT T_id FROM Basket
            WHERE B_id_hashed = {b_id}
        """)

    for it_ in result:
        simple_sql(f"""
            UPDATE Ticket SET Sold = TRUE WHERE T_id = {it_}
        """)

    simple_sql(f"""
        UPDATE Basket SET B_paid = NOW() WHERE B_id_hashed = {b_id}
    """)
    return


# def return_cart(query_):
#     return


def simple_sql(query_):
    with UseDatabase(current_app.config['dbconfig']) as cursor:
        cursor.execute(query_, )
        return cursor.fetchall()
