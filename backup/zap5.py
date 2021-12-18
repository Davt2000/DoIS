import json
import mysql.connector
from flask import render_template, request, current_app, session
from flask import Blueprint
from utilities.usedatabase import UseDatabase
sp5_blueprint = Blueprint('sp5_blueprint', __name__, template_folder='templates')


@sp5_blueprint.route('/zap5', methods=['GET', 'POST'])
def sob_bp():
    if 'user' in session:
        if (session['user']==[('director',)]):
            return render_template('NOT.html')
    else:
        return render_template('NOT.html')
    with open('data/dbconfig.json', 'r', encoding='utf-8') as f:
        current_app.config['dbconfig']=json.load(f)
    try:
        buttom = request.args('send6')
    except:
        buttom = request.form.get('send6')
    if (buttom is not None):
        nam=request.form.get('nam')
        numb=request.form.get('numb')
        with UseDatabase(current_app.config['dbconfig']) as cursor:
            _SQL = """SELECT %s*menu_price, %s*menu_weight, %s, %s from menu where menu_name=%s;""" 
            cursor.execute(_SQL,(int(numb), int(numb), nam, numb, nam))
            result1 = cursor.fetchall()
            res1 = []
            schema1 = ['price', 'weight', 'name','number']
        for line1 in result1:
            res1.append(dict(zip(schema1, line1)))
        return render_template('res5.html', films=res1)
    else:
        with UseDatabase(current_app.config['dbconfig']) as cursor:
            _SQL = """SELECT menu_id, menu_weight, menu_number, menu_price, menu_name FROM menu""" 
            cursor.execute(_SQL,)
            result = cursor.fetchall()
            res = []
            schema = ['menu_id', 'menu_weight', 'menu_number','menu_price', 'menu_name']
        for line in result:
            res.append(dict(zip(schema, line)))
        if (result==[]):
            return render_template('zap5.html')
        return render_template('zap5.html', films=res)