from peewee import *
from os import path


connection = path.dirname(path.realpath(__file__))
db = SqliteDatabase(path.join(connection, 'borrow-log.db'))


class Borrow(Model):
    name = CharField()
    book = CharField()
    date = CharField()
    status = CharField()

    class Meta:
        database = db


Borrow.create_table(fail_silently=True)