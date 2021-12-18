from flask import session, redirect, request
from functools import wraps
import json


def decor(f):
    def wrapper(*args, **kwargs):
        print('before')
        return f(*args, **kwargs)
    return wrapper


def in_session(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'user' in session:
            return f(*args, **kwargs)
        return redirect('/login')

    return wrapper


def has_valid_group():
    group_name = session.get('role', '')
    with open('data/access.json', 'r', encoding='utf-8') as f:
        access_list = json.load(f)
    target_app = "" if len(request.endpoint.split(".")) == 1 else request.endpoint.split('.')[0]  # gets target bp name
    if group_name in access_list and target_app in access_list[group_name]:
        return True
    else:
        return False


def group_valid_dec(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if has_valid_group():
            return f(*args, **kwargs)
        return redirect('/')
    return wrapper


