import json
from flask import request, current_app
from flask import Blueprint, session, render_template
from utilities.usedatabase import UseDatabase
from utilities.check_authority import in_session

grid_editor_blueprint = Blueprint('grid_editor_blueprint', __name__, template_folder='templates')


@grid_editor_blueprint.route('/', methods=['GET', 'POST'])
@in_session
def grid_editor():
    with open('data/dbconfig.json', 'r', encoding='utf-8') as f:
        current_app.config['dbconfig'] = json.load(f)
    add = request.form.get('add')
    remove = request.form.get('del')
    if add:
        country = request.form.get('Country')
        year = request.form.get('Year')
        director = request.form.get('Director')
        studio = request.form.get('Studio')
        length = request.form.get('Length')
        name = request.form.get('Name')

        if country and year and director and studio and length and name:
            with UseDatabase(current_app.config['dbconfig']) as cursor:
                _SQL = f"""INSERT INTO Film(Country, Year, Director, Studio, Length, Name) 
                            VALUES ('{country}', {year}, '{director}', '{studio}', {length}, '{name}')
                                """
                cursor.execute(_SQL, )
    elif remove:
        with UseDatabase(current_app.config['dbconfig']) as cursor:
            _SQL = f"""DELETE FROM Film
                WHERE F_id = {request.form.get('id_to_delete')}
                """
            cursor.execute(_SQL,)
    with UseDatabase(current_app.config['dbconfig']) as cursor:
        _SQL = """SELECT *
            FROM
            Film
            """
        cursor.execute(_SQL,)
        result = cursor.fetchall()
        res = []
        schema = ['F_id', 'Country', 'Year', 'Director', 'Studio', 'Length', 'Name']

    for line in result:
        res.append(dict(zip(schema, line)))
    return render_template("editor.html", items=res, usr=session['user'])
