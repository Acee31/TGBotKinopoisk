from datetime import datetime

from peewee import (
    CharField,
    ForeignKeyField,
    IntegerField,
    Model,
    SqliteDatabase,
    DateTimeField
)

from config_data.config import DB_PATH

db = SqliteDatabase(DB_PATH)


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    user_id = IntegerField(primary_key=True)
    username = CharField(null=True)
    first_name = CharField(null=True)
    last_name = CharField(null=True)


class History(BaseModel):
    user = ForeignKeyField(User, backref="history")
    search_date = DateTimeField(default=datetime.now)
    title = CharField()
    description = CharField(null=True)
    rating = CharField(null=True)
    year = IntegerField(null=True)
    genre = CharField(null=True)
    adult_rating = CharField(null=True)
    poster = CharField(null=True)


def create_models():
    db.create_tables(BaseModel.__subclasses__())

