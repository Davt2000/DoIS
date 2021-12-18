import json
from flask import render_template, request, current_app, session
from flask import Blueprint
from utilities.usedatabase import UseDatabase

sp1_blueprint = Blueprint('sp1_blueprint', __name__, template_folder='templates')


@sp1_blueprint.route('/', methods=['GET', 'POST'])
def sob_bp():
    if 'user' in session:
        #  check authority
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
    else:
        return render_template('NOT.html')
