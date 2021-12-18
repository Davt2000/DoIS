import json
import mysql.connector
from flask import render_template, request, current_app, session
from flask import Blueprint
from utilities.usedatabase import UseDatabase
sp3_blueprint = Blueprint('sp3_blueprint', __name__, template_folder='templates')


@sp3_blueprint.route('/zap3', methods=['GET', 'POST'])
def sob_bp():
    if 'user' in session:
        if (session['user']!=[('admin',)]):
            return render_template('NOT.html')
    else:
        return render_template('NOT.html')
    with open('data/dbconfig.json', 'r', encoding='utf-8') as f:
        current_app.config['dbconfig'] = json.load(f)
    try:
        buttom = request.args('send')
    except:
        buttom=None
        pas=None
        ofid=None
        numb=None
        nam=None
        dat=None
        birth=None
        delet=None
        buttom = request.form.get('send')
    if (buttom is not None):
        ofid=request.form.get('id')
        numb=request.form.get('numb')
        nam=request.form.get('nam')
        dat=request.form.get('dat')
        birth=request.form.get('birth')
        with UseDatabase(current_app.config['dbconfig']) as cursor:
            _SQL = """INSERT INTO oficiant values(%s, %s, %s, %s, %s);""" 
            cursor.execute(_SQL,(int(ofid), int(numb), nam, int(dat), int(birth)))
    try:
        buttom2 = request.args('send2')
    except:
        buttom2=None
        delet=None
        buttom2 = request.form.get('send2')
    if (buttom2 is not None):
        delet=request.form.get('delet')
        with UseDatabase(current_app.config['dbconfig']) as cursor:
            _SQL = """DELETE FROM oficiant WHERE of_number=%s;""" 
            cursor.execute(_SQL,(int(delet), ))
    buttom=None
    buttom2=None
    delet=None
    ofid=None
    numb=None
    nam=None
    dat=None
    birth=None
    buttom=None
    with UseDatabase(current_app.config['dbconfig']) as cursor:
        _SQL = """SELECT of_id, of_number, of_name, of_date, of_birth FROM oficiant""" 
        cursor.execute(_SQL,)
        result = cursor.fetchall()
        res = []
        schema = ['of_id', 'of_number', 'of_name','of_date', 'of_birth']
        if (result==[('emp',)]):
            print ('Error')
    for line in result:
        res.append(dict(zip(schema, line)))
    if (result==[]):
        return render_template('zap3.html')
    return render_template('zap3.html', films=res)