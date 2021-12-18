import json

from flask import render_template, request, current_app
from flask import Blueprint
from utilities.usedatabase import UseDatabase
sp2_blueprint = Blueprint('sp2_blueprint', __name__, template_folder='templates')

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


@sp2_blueprint.route('/', methods=['GET', 'POST'])
def sob_bp():
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
