import json
import mysql.connector
from flask import render_template, request, current_app, session
from flask import Blueprint
from utilities.usedatabase import UseDatabase
sp4_blueprint = Blueprint('sp4_blueprint', __name__, template_folder='templates')


@sp4_blueprint.route('/zap4', methods=['GET', 'POST'])
def sob_bp():
    if 'user' in session:
        if session['user'] != [('admin',)]:
            return render_template('NOT.html')
    else:
        return render_template('NOT.html')
    with open('data/dbconfig.json', 'r', encoding='utf-8') as f:
        current_app.config['dbconfig']=json.load(f)
    try:
        buttom = request.args('send1')
    except:
        buttom = request.form.get('send1')
    if (buttom is not None):
        menuid=request.form.get('menuid')
        weight=request.form.get('weight')
        mnumb=request.form.get('mnumb')
        mprice=request.form.get('mprice')
        menunam=request.form.get('menunam')
        with UseDatabase(current_app.config['dbconfig']) as cursor:
            _SQL = """INSERT INTO menu values(%s, %s, %s, %s, %s);""" 
            cursor.execute(_SQL,(int(menuid), int(weight), int(mnumb), int(mprice), menunam))
    try:
        buttom2 = request.args('send12')
    except:
        buttom2=None
        delet=None
        buttom2 = request.form.get('send12')
    if (buttom2 is not None):
        delet=request.form.get('mdelet')
        with UseDatabase(current_app.config['dbconfig']) as cursor:
            _SQL = """DELETE FROM menu WHERE menu_id=%s;""" 
            cursor.execute(_SQL,(int(delet), ))
    buttom=None
    buttom2=None
    delet=None
    menuid=None
    weight=None
    numb=None
    price=None
    nam=None
    with UseDatabase(current_app.config['dbconfig']) as cursor:
        _SQL = """SELECT menu_id, menu_weight, menu_number, menu_price, menu_name FROM menu""" 
        cursor.execute(_SQL,)
        result = cursor.fetchall()
        res = []
        schema = ['menu_id', 'menu_weight', 'menu_number','menu_price', 'menu_name']
        if (result==[('emp',)]):
            print ('Error')
    for line in result:
        res.append(dict(zip(schema, line)))
    if (result==[]):
        return render_template('zap4.html')
    return render_template('zap4.html', films=res)