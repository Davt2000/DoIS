from flask import Blueprint, session, redirect,\
    render_template, request, url_for
import json
with open('data/queries.json', 'r', encoding='utf-8') as f:
    main_menu = json.load(f)

menu_blueprint = Blueprint('menu_blueprint', __name__, template_folder='templates')


@menu_blueprint.route('/', methods=['GET'])
def menu():
    if 'user' in session:
        rout_mapping = {
            '1': url_for('auth_blueprint.auth'),
            '2': url_for('sp1_blueprint.sob_bp'),
            '3': url_for('sp2_blueprint.sob_bp'),
            '4': url_for('sp3_blueprint.sob_bp'),
            '5': url_for('sp4_blueprint.sob_bp'),
            '6': url_for('sp5_blueprint.sob_bp'),
            '7': url_for('sp6_blueprint.sob_bp')
            }
        point = request.args.get('point')
        if point is None:
            return render_template('menu.html', kino=main_menu, usr=session['user'][0][0])
        elif point in rout_mapping:
            return redirect(rout_mapping[point])
        else:
            name_to_send = session['user'][0][0]
            session.pop('user')
            return render_template('logoff.html', usr=name_to_send)
    else:
        return redirect('/login')