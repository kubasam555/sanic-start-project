from functools import wraps

from sanic.response import redirect
from settings import session
from core.models import User


def auth_user(request, user: User):
    user_dict = {
        'username': user.username,
        'is_authenticated': True
    }
    request['session']['user'] = user_dict


def logout_user(request):
    del request['session']['user']


def login_required(f):
    @wraps(f)
    def inner(request, *args, **kwargs):
        if not request['session'].get('user'):
            return redirect(request.app.url_for('root'))
        return f(*args, **kwargs)
    return inner


def class_login_required(f):
    @wraps(f)
    def inner(view, request, *args, **kwargs):
        if not request['session'].get('user'):
            return redirect(request.app.url_for('root'))
        return f(view, request, *args, **kwargs)

    return inner
