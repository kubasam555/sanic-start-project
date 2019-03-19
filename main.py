import os

from sanic.exceptions import abort
from sanic.log import logger
from sanic.response import json, stream, text
from sanic.response import redirect

from core.models import AuthToken
from core.models import User
from core.utils import auth_user
from settings import app
from apps.auth.main import auth_bp
from apps.post.main import post_bp
from create_tables import create_tables


app.blueprint(auth_bp)
app.blueprint(post_bp)
app.static('/static', './static')

DEBUG = os.environ.get('DEBUG') == 'True'


@app.middleware('request')
async def middleware_session_request(request):
    if DEBUG:
        logger.info(f'Middleware request: {str(request.get("session"))}')


@app.middleware('response')
async def middleware_session_response(request, response):
    if DEBUG:
        logger.info(f'Middleware response: {str(request.get("session"))}')


@app.middleware('request')
async def middleware_token_auth(request):
    try:
        token_key, token = request.headers.get('Authorization').split()
        if not token_key == 'Token':
            return
        user = AuthToken.get(AuthToken.token == token).user
        auth_user(request, user)
    except (AttributeError, ValueError, AuthToken.DoesNotExist):
        pass


# @app.middleware('request')
# async def authenticate_middleware(request):
#     session_user = request['session'].get('user')
#     if session_user:
#         try:
#             user = User.get(User.username == session_user['username'])
#         except User.DoesNotExist:
#             pass
#         else:
#             request['user'] = user
#     # return request


@app.route("/")
async def root(request):
    return json({"hello": "world"})


# create_tables()

if __name__ == "__main__":
    WORKERS = int(os.environ.get('WORKERS', 1))
    # app.run(host="0.0.0.0", port=8000, debug=False)
    app.run(host="0.0.0.0", port=8000, debug=DEBUG, workers=WORKERS)
