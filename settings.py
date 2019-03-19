import os

from peewee import PostgresqlDatabase
from sanic import Sanic
from sanic_session import InMemorySessionInterface
from sanic_session import Session


app = Sanic()
app.config.ACCESS_LOG = False
session = Session(app, interface=InMemorySessionInterface())

database = PostgresqlDatabase(
    os.environ['POSTGRES_DB'],
    user=os.environ['POSTGRES_USER'],
    password=os.environ['POSTGRES_PASSWORD'],
    host=os.environ['POSTGRES_HOST'],
    port=os.environ['POSTGRES_PORT']
)


@app.middleware('request')
async def middleware_db_request(request):
    database.connect()


@app.middleware('response')
async def middleware_db_response(request, response):
    database.close()
    return response
