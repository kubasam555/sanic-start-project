from datetime import datetime
from hashlib import md5
from uuid import uuid4

import peewee
from playhouse.signals import post_save

from settings import database


class BaseModel(peewee.Model):
    class Meta:
        database = database


class User(BaseModel):
    username = peewee.CharField(unique=True)
    password = peewee.CharField()
    join_date = peewee.DateTimeField(default=datetime.now, null=True)

    def check_password(self, password: str):
        pw_hash = md5(password.encode('utf-8')).hexdigest()
        return self.password == pw_hash

    @classmethod
    def create(cls, **query):
        query['join_date'] = datetime.now()
        instance = super().create(**query)
        AuthToken.create(
            user=instance
        )
        return instance


class Post(BaseModel):
    user = peewee.ForeignKeyField(User, backref='posts')
    title = peewee.CharField(max_length=255)
    content = peewee.CharField(max_length=1023)


class AuthToken(BaseModel):
    user = peewee.ForeignKeyField(User, backref='auth_token', unique=True)
    token = peewee.CharField(max_length=255, )

    @classmethod
    def create(cls, **query):
        token = uuid4().hex
        while cls.select().where(cls.token == token).exists():
            token = uuid4().hex
        query['token'] = token
        return super().create(**query)

