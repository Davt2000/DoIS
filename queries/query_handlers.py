import json
from flask import render_template, request, current_app, session
from flask import Blueprint
from utilities.usedatabase import UseDatabase
from utilities.check_authority import in_session

query_handlers_blueprint = Blueprint('query_handlers_blueprint', __name__, template_folder='templates')


@query_handlers_blueprint.route('/query1', methods=['GET', 'POST'])
@in_session
def handler1():
    with open('data/dbconfig.json', 'r', encoding='utf-8') as f:
        current_app.config['dbconfig'] = json.load(f)
    date = request.form.get('date')
    if date:
        with UseDatabase(current_app.config['dbconfig']) as cursor:
            _SQL = """SELECT
                H.Name, TIME(Se.Data), SUM(T.Price)
                FROM
                Ticket T JOIN Scheme Sc on T.Sc_id = Sc.Sc_id JOIN Hall H on Sc.H_id = H.H_id
                JOIN Session Se on H.H_id = Se.H_id JOIN Film F on Se.F_id = F.F_id
                WHERE
                DATE(Se.Data)=%s AND T.Sold = 1 GROUP BY Se.Se_id;"""
            cursor.execute(_SQL, (date,))
            result = cursor.fetchall()
            res = []
            schema = ['HallName', 'SessTime', 'Total']
            if result == [('emp',)]:
                print('Error')
        for line in result:
            res.append(dict(zip(schema, line)))
        if not result:
            return render_template('zap1.html')
        return render_template('res1.html', films=res)

    else:
        return render_template('zap1.html')


month_bruteforce = {
    '01': 31,
    '02': 28,
    '03': 31,
    '04': 30,
    '05': 31,
    '06': 30,
    '07': 30,
    '08': 31,
    '09': 30,
    '10': 31,
    '11': 30,
    '12': 31
}


@query_handlers_blueprint.route('/query2', methods=['GET', 'POST'])
def handler2():
    with open('data/dbconfig.json', 'r', encoding='utf-8') as f:
        current_app.config['dbconfig'] = json.load(f)
    date1 = request.form.get('date')
    if date1:
        date1 = date1[:-2] + '01'
        if int(date1[5:7]) == 2 and int(date1[:4]) % 4 == 0 and int(date1[:4]) % 100 != 0:
            date2 = date1[:-2] + '29'
        else:
            date2 = date1[:-2] + str(month_bruteforce[date1[5:7]])
        print(date1, date2)
        with UseDatabase(current_app.config['dbconfig']) as cursor:
            _SQL = """SELECT Data, SUM(Price)
                FROM Ticket T JOIN Session Se
                WHERE Se.Se_id = T.Se_id AND Sold = 1 AND %s <= Data AND Data < %s
                GROUP BY Data"""
            cursor.execute(_SQL, (date1, date2))
            result = cursor.fetchall()
            res = []
            schema = ['Date', 'Total']
            if result == [('emp',)]:
                print('Error')
        for line in result:
            res.append(dict(zip(schema, line)))
        if not result:
            return render_template('zap2.html')
        return render_template('res2.html', films=res, rep=date1[:-3])
    else:
        return render_template('zap2.html')


@query_handlers_blueprint.route('/query3', methods=['GET', 'POST'])
def handler3():
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


@query_handlers_blueprint.route('/query4', methods=['GET', 'POST'])
def handler4():
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


@query_handlers_blueprint.route('/query5', methods=['GET', 'POST'])
def handler5():
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


@query_handlers_blueprint.route('/query6', methods=['GET', 'POST'])
def handler6():
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
