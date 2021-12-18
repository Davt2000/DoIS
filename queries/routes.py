from flask import Blueprint, session, redirect,\
    render_template, request, url_for
import json
from utilities.check_authority import in_session, group_valid_dec
with open('data/queries.json', 'r', encoding='utf-8') as f:
    main_menu = json.load(f)

query_routing_blueprint = Blueprint('query_routing_blueprint', __name__, template_folder='templates')


@query_routing_blueprint.route('/', methods=['GET'])
@in_session
@group_valid_dec
def menu():
    if 'user' in session:
        rout_mapping = {
            '1': url_for('query_handlers_blueprint.handler1'),
            '2': url_for('query_handlers_blueprint.handler2'),
            '3': url_for('query_handlers_blueprint.handler3'),
            '4': url_for('query_handlers_blueprint.handler4'),
            '5': url_for('query_handlers_blueprint.handler5'),
            '6': url_for('query_handlers_blueprint.handler6')
            }
        point = request.args.get('point')
        if point is None:
            return render_template('menu_query.html', kino=main_menu, usr=session['user'])
        elif point in rout_mapping:
            return redirect(rout_mapping[point])
    else:
        return redirect('/login')
