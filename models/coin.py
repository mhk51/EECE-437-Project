from ..app import db, bcrypt, ma
import datetime

class Coin(db.Model):
    __table_args__ = (
        db.UniqueConstraint('coin_id', 'coin_name', name='unique_component_commit'),
    )
    coin_id = db.Column(db.Integer, primary_key=True)
    coin_name = db.Column(db.String(30))
    added_date = db.Column(db.DateTime, primary_key=True)
    coin_price = db.Column(db.Float, nullable=False)
    coin_24h_change = db.Column(db.Float, nullable=False)
    
    def __init__(self, id, name, coin_price, coin_24h_change):
        super(Coin, self).__init__(coin_id=id,
                                   coin_name=name,
                                   coin_price=coin_price,
                                   coin_24h_change=coin_24h_change,
                                   added_date=datetime.datetime.now()
                                   )


class CoinSchema(ma.Schema):
    class Meta:
        fields = ("coin_id", "coin_name", "added_date", "coin_price", "coin_24h_change")
        model = Coin