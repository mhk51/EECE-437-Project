from ..app import db, bcrypt, ma
import datetime

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    added_date = db.Column(db.DateTime)
    coin_id = db.Column(db.Integer, db.ForeignKey('coind.coin_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    bot_id = db.Column(db.Integer, db.ForeignKey('bot.bot_id'), nullable=True)

    def __init__(self, amount, coin_id, user_id, bot_id):
        super(Transaction, self).__init__(amount=amount,
                                          coin_id=coin_id,
                                          user_id=user_id,
                                          bot_id=bot_id,
                                          added_date=datetime.datetime.now())


class TransactionSchema(ma.Schema):
    class Meta:
        fields = ("id", "amount", "coin_id", "added_date", "user_id", "bot_id")
        model = Transaction