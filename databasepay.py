from peewee import *
from os import path

connect = path.dirname(path.realpath(__file__))
db = SqliteDatabase(path.join(connect, "myLibPay.db"))


class Payments(Model):
    name = CharField()
    file = CharField()
    amount = CharField()

    class Meta:
        database = db


Payments.create_table(fail_silently=True)