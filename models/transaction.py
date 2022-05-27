from re import U
from app import db, bcrypt, ma
import datetime

from .user import User

class Transaction(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date = db.Column(db.DateTime)
    coin_amount = db.Column(db.Float,nullable=False)
    usd_amount = db.Column(db.Float, nullable=False)
    exchange_rate = db.Column(db.Float,nullable=False)
    coin_name = db.Column(db.String(30),nullable=False)
    buying = db.Column(db.Boolean,nullable=False)
    user_total = db.Column(db.Float,nullable=False)

    def __init__(self,user_id, exchange_rate,buying,coin_name,coin_amount,usd_amount,user_total):
        super(Transaction, self).__init__(exchange_rate=exchange_rate,
                                          coin_name=coin_name,
                                          coin_amount=coin_amount,
                                          usd_amount=usd_amount,
                                          buying=buying,
                                          user_id=user_id,
                                          user_total=user_total,
                                          date=datetime.datetime.now())

class TransactionSchema(ma.Schema):
    class Meta:
        fields = ("id","user_id","date","coin_amount","usd_amount","exchange_rate","coin_name","buying","user_total")
        model = Transaction