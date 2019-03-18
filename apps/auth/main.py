from hashlib import md5
from sanic import Blueprint
from sanic.response import json
from sanic.response import redirect

from core.models import User
from core.utils import auth_user
from core.utils import logout_user

auth_bp = Blueprint('auth_app', url_prefix='/auth')


@auth_bp.route('/login', methods=['GET', 'POST'])
async def login(request):
    if request.method == 'POST':
        username = request.json.get('username')
        password = request.json.get('password')

        user = User.select().where(User.username == username)
        if not user.exists() or not user[0].check_password(password):
            return json({'error': 'Authentication failed'})

        auth_user(request, user[0])
    return redirect(request.app.url_for('root'))


@auth_bp.route('/register', methods=['GET', 'POST'])
async def register(request):
    if request.method == 'POST':
        username = request.json.get('username')
        password = request.json.get('password')

        user = User.select().where(User.username == username)
        if user.exists():
            return json({'error': 'Username exists in database'})

        User.create(
            username=username,
            password=md5(password.encode('utf-8')).hexdigest()
        )
    return redirect(request.app.url_for('auth_app.login'))


@auth_bp.route('/logout', methods=['GET'])
async def logout(request):
    logout_user(request)
    return redirect(request.app.url_for('root'))





