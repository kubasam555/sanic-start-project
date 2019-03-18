from datetime import datetime
from hashlib import md5

import peewee
from settings import database


class BaseModel(peewee.Model):
    class Meta:
        database = database


class User(BaseModel):
    username = peewee.CharField(unique=True)
    password = peewee.CharField()
    join_date = peewee.DateTimeField(default=datetime.now, null=None)

    def check_password(self, password: str):
        pw_hash = md5(password.encode('utf-8')).hexdigest()
        return self.password == pw_hash

    @classmethod
    def create(cls, **query):
        query['join_date'] = datetime.now()
        return super().create(**query)


class Post(BaseModel):
    user = peewee.ForeignKeyField(User, backref='posts')
    title = peewee.CharField(max_length=255)
    content = peewee.CharField(max_length=1023)


