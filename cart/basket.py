import json
import mysql.connector
import mysql.connector.errors
from flask import Flask, render_template,request,redirect, url_for, session
from flask import render_template, request, current_app
from flask import Blueprint, session, redirect, render_template
from utilities.usedatabase import UseDatabase, ConnectionError, SQLError, DataError
from utilities.check_authority import in_session


item = [
    {'id': 1, 't_name': 'Check1'},
    {'id': 2, 't_name': 'Check2'},
    {'id': 3, 't_name': 'Check3'}
    ]

cart_blueprint_ = Blueprint('cart_blueprint_', __name__, template_folder='templates')


@cart_blueprint_.route('/', methods=['GET', 'POST'])
@in_session
def cho():
    exit = None
    result = None
    choise_id = None
    choise_name = None

    delete = request.form.get('delete')
    show = request.form.get('Check1')

    if show:
        result=show
        choise_id=1
        choise_name='Check1'

    show=request.form.get('Check2')

    if show:
        result=show
        choise_id=2
        choise_name='Check2'

    show=request.form.get('Check3')

    if show:
        result=show
        choise_id=3
        choise_name='Check3'
    if result:
        exit=put_in_cart(result, choise_id, choise_name, exit)
    show=request.form.get('exit')
    exit=request.form.get('show_basket')
    if exit:
        if 'cart' in session:
            return render_template('cart.html', items=session['cart'])
        else:
            return render_template('delete.html')
    if show:
        if 'cart' in session:
            k=save_cart()
            if (k=="Error"):
                return "Error"
            if (k=="Data error"):
                return "Data error"
            if (k=="Ошибка выполнения запроса"):
                return "Ошибка выполнения запроса"
        if 'cart' in session:
            session.pop('cart')
        return redirect('/menu')
    if delete:
        if 'cart' in session:
            k=save_cart()
            if (k=="Error"):
                return "Error"
            if (k=="Data error"):
                return "Data error"
            if (k=="Ошибка выполнения запроса"):
                return "Ошибка выполнения запроса"
        if 'cart' in session:
            session.pop('cart')
        return render_template('delete.html')
    else:
        return render_template('choice_list.html', items=item)


def put_in_cart(quantity, choice_id, choice_name, leng):
    if 'cart' in session:
        session['cart']+=[{
            'choice_id' : int(choice_id),
            'choice_name': choice_name,
            'quantity' : int(quantity),}]
    else:
        session['cart']=[{
            'choice_id' : int(choice_id),
            'choice_name': choice_name,
            'quantity' : int(quantity),}]
    basket_len = len(session['cart'])
    return basket_len


def save_cart():
    basket_len = len(session['cart'])
    print(basket_len)
    try:
        with open('F:/Python/Python/lab3/data/dbconfig.json','r',encoding='utf-8') as f: 
            current_app.config['dbconfig']=json.load(f)
        _SQL = """insert  into Basket values(%s,%s,%s)"""
        with UseDatabase(current_app.config['dbconfig']) as cursor:
            for i in range(basket_len):
                values = session['cart'][i].values()
                values = list(values)
                cursor.execute(_SQL,(values[0],values[1],values[2],))
    except ConnectionError as err:
        return "Error"
    except DataError as err:
        return "Data error"
    except SQLError as err:
        print("Ошибка выполнения запроса",str(err))
        str_err = "Ошибка выполнения запроса"
        return str_err
    return
