import json
from flask import request, current_app
from flask import Blueprint, session, render_template
from utilities.usedatabase import UseDatabase
from utilities.check_authority import in_session

cart_blueprint = Blueprint('cart_blueprint', __name__, template_folder='templates')


@cart_blueprint.route('/', methods=['GET', 'POST'])
@in_session
def start_handler():
    update_session_cart(abs(hash(session['user'])%10000))  # potentially insecure hash
    if 'user' in session:
        rol = session['role']
        usr = session['user']
    else:
        rol = 'Unauthorized'
        usr = 'user'
    return render_template("marketplace_index.html", rol=rol, usr=usr)


@cart_blueprint.route('/list', methods=['GET', 'POST'])
@in_session
def session_handler():  # do not confuse movie session (business object) and flask.session
    return render_template('sessions_list_b.html', usr=session['user'], items=get_available_sessions())


@cart_blueprint.route('/tickets', methods=['GET', 'POST'])
@in_session
def ticket_handler():
    se_id = request.args.get('id')
    all_tickets = get_available_tickets(se_id)

    if request.method == "POST":
        t_id = request.form.get('id_to_add')

        if t_id not in session['cart']:
            item_to_put = simple_sql(
                f""" SELECT F.Name, T.Price
                    FROM Session Se 
                    JOIN Film F on F.F_id = Se.F_id  
                    JOIN Ticket T on Se.Se_id = T.Se_id
                    WHERE T.T_id = {t_id}
                """
            )
            cart = session['cart']
            cart[t_id] = {
                "F_name": item_to_put[0][0],
                "T_price": item_to_put[0][1],
                "B_item_id": None,
                "B_paid": None,
                "T_id": t_id
            }
            session['cart'] = cart

    return render_template('ticket_list.html', usr=session['user'], items=all_tickets)


@cart_blueprint.route('/cart', methods=['GET', 'POST'])
@in_session
def cart_handler():
    with open('data/dbconfig.json', 'r', encoding='utf-8') as f:
        current_app.config['dbconfig'] = json.load(f)

    b_id = abs(hash(session['user'])%10000)     # potentially unsafe and even more insecure
    update_session_cart(b_id)

    buy = request.form.get('buy')
    remove = request.form.get('del')
    drop = request.form.get('drop')

    if remove:
        cart = session['cart']
        cart.pop(request.form.get('id_to_delete'))
        session['cart'] = cart
    if drop:
        session['cart'] = dict()
        drop_cart(b_id)
    if buy:
        save_cart(session['cart'], b_id)
        buy_all(b_id)
        drop_cart(b_id)
        session['cart'] = dict()

    cart = session['cart'].values()
    count_ = 0
    to_pay = 0
    for i in cart:
        count_ += 1
        to_pay += i['T_price']
    return render_template('cart_base.html', items=cart,
                           usr=session['user'], count_=count_, to_pay=to_pay)


def get_available_sessions():
    result = simple_sql(f"""
        SELECT Se.Se_id, F.Name, H.Name, Se.Data 
        FROM Session Se 
        JOIN Film F on F.F_id = Se.F_id  
        JOIN Hall H on H.H_id = Se.H_id
        WHERE Se.Data >= NOW()
    """)
    res = []
    schema = ['id', 'film', 'hall', 'datetime']
    for line in result:
        res.append(dict(zip(schema, line)))
    return res


def get_available_tickets(se_id):
    result = simple_sql(f"""
        SELECT T.T_id, T.Price, Sc.Row_, Se.Data, F.Name
        FROM Ticket T 
        JOIN Session Se on T.Se_id = Se.Se_id
        JOIN Scheme Sc on Sc.Sc_id = T.Sc_id
        JOIN Film F on F.F_id = Se.F_id
        WHERE Se.Se_id = {se_id} AND T.Sold = FALSE
    """)
    res = []
    schema = ['T_id', 'T_Price', 'row_', 'date', 'F_name']
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
    session['cart'].pop(request.form.get('id_to_delete'))
    return


def drop_cart(b_id):
    with UseDatabase(current_app.config['dbconfig']) as cursor:
        cursor.execute(f"""
    DELETE FROM Basket WHERE B_id_hashed = {b_id}""",)
    return


def save_cart(cart_content, b_id):
    drop_cart(b_id)
    for it_ in cart_content:
        namae = cart_content[it_]["F_name"]
        with UseDatabase(current_app.config['dbconfig']) as cursor:
            cursor.execute(f"""
            INSERT INTO Basket (B_id_hashed, F_name, T_price, T_id)
            VALUES ({b_id}, '{namae}', {cart_content[it_]["T_price"]}, {cart_content[it_]["T_id"]}) 
        """,)
    return


def buy_all(b_id):
    result = simple_sql(f"""
            SELECT T_id FROM Basket
            WHERE B_id_hashed = {b_id}
        """)

    for it_ in result:
        update_sql(f"""
            UPDATE Ticket SET Sold = TRUE WHERE T_id = {it_[0]}
        """)

    update_sql(f"""
        UPDATE Basket SET B_paid = NOW() WHERE B_id_hashed = {b_id}
    """)
    return


# def return_cart(query_):
#     return


@cart_blueprint.before_request
def load_user():
    with open('data/dbconfig.json', 'r', encoding='utf-8') as f:
        current_app.config['dbconfig'] = json.load(f)


def update_sql(query_):
    with UseDatabase(current_app.config['dbconfig']) as cursor:
        cursor.execute(query_, )
    return


def simple_sql(query_):

    with UseDatabase(current_app.config['dbconfig']) as cursor:
        cursor.execute(query_, )
        return cursor.fetchall()


def update_session_cart(b_id):
    cart = session.get('cart', dict())

    if not cart.keys():
        cart = get_cart(b_id)
        if cart == ('emp',):
            cart = dict()  # ¯\_(ツ)_/¯
    else:
        save_cart(cart, b_id)
    session['cart'] = cart