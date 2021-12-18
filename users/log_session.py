from flask import Blueprint, session, redirect,\
    render_template, request, current_app
import json

from utilities.usedatabase import UseDatabase
from utilities.check_authority import in_session

auth_blueprint = Blueprint('auth_blueprint', __name__, template_folder='templates')


@auth_blueprint.route('/', methods=['POST', 'GET'])
def auth():
    with open('data/dbconfig.json', 'r', encoding='utf-8') as f:
        current_app.config['dbconfig'] = json.load(f)
    if request.method == 'POST':
        log = request.form.get('login')
        if log is not None and log != "":
            pas = request.form.get('password')

            with UseDatabase(current_app.config['dbconfig']) as cursor:
                _SQL = """select u_login, r_name 
                FROM Users U JOIN Roles_Users RU on U.u_id = RU.u_id JOIN Roles R on R.r_id = RU.r_id
                where U_LOGIN= %s and U_PSWRD=%s;"""

                cursor.execute(_SQL, (log, pas))
                result = cursor.fetchall()
                if result == [('emp',)]:
                    print('Error')
                    return render_template('auth.html')
            if not result:
                return render_template('auth.html')

            session.clear()
            session['user'] = result[0][0]
            session['role'] = result[0][1]
            return redirect('/')

        return render_template('auth.html')
    else:
        return render_template('log.html')


@auth_blueprint.route('/exit', methods=['POST', 'GET'])
@in_session
def logoff():
    name_to_send = session['user']
    session.clear()
    return render_template('logoff.html', usr=name_to_send)


def get_user_role():
    with open('data/dbconfig.json', 'r', encoding='utf-8') as f:
        current_app.config['dbconfig'] = json.load(f)