from app import db, bcrypt, ma
import datetime

class Coin(db.Model):
    __table_args__ = (
        db.UniqueConstraint('coin_name','date', name='unique_component_commit'),
    )
    coin_name = db.Column(db.String(30),primary_key=True)
    date = db.Column(db.DateTime, primary_key=True)
    price_open = db.Column(db.Float, nullable=False)
    price_high = db.Column(db.Float,nullable=False)
    price_low = db.Column(db.Float,nullable = False)
    price_close = db.Column(db.Float, nullable=False)
    volume = db.Column(db.Float,nullable = False)  



    def __init__(self, name,price_open,price_high,price_low,price_close,volume,date):
        super(Coin, self).__init__(
                                   coin_name=name,
                                   price_open = price_open,
                                   price_high = price_high,
                                   price_low = price_low,
                                   price_close = price_close,
                                   volume = volume,
                                   date=date
                                   )


class CoinSchema(ma.Schema):
    class Meta:
        fields = ("coin_name", "date",'price_open','price_high','price_low','price_close','volume')
        model = Coin