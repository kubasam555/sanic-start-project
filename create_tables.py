# simple utility function to create tables
from core.models import AuthToken
from core.models import Post
from core.models import User
from settings import database


def create_tables():
    with database:
        database.create_tables([AuthToken])
