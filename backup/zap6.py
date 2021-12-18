import json
import mysql.connector
from flask import render_template, request, current_app, session
from flask import Blueprint
from utilities.usedatabase import UseDatabase
sp6_blueprint = Blueprint('sp6_blueprint', __name__, template_folder='templates')


@sp6_blueprint.route('/zap6', methods=['GET', 'POST'])
def sob_bp():
    if 'user' in session:
        if (session['user']!=[('admin',)]):
            return render_template('NOT.html')
    else:
        return render_template('NOT.html')
    with open('data/dbconfig.json', 'r', encoding='utf-8') as f:
        current_app.config['dbconfig']=json.load(f)
    try:
        buttom = request.args('send')
    except:
        buttom=None
        year=None
        buttom = request.form.get('send')
    if (buttom is not None):
        year=request.form.get('year')
        with UseDatabase(current_app.config['dbconfig']) as cursor:
            _SQL = """SELECT ord_id, of_id, ord_sum, ord_date FROM ord WHERE YEAR(ord_date)=%s;""" 
            cursor.execute(_SQL,(year,))
            result = cursor.fetchall()
            res = []
            schema = ['ord_id', 'of_id', 'ord_sum','ord_date']
            if (result==[('emp',)]):
                print ('Error')
        for line in result:
            res.append(dict(zip(schema, line)))
        if (result==[]):
            return render_template('zap6.html')
        return render_template('res6.html', films=res)
    else:
        return render_template('zap6.html')