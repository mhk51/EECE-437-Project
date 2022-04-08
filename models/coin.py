from ..app import db, bcrypt, ma
import datetime

class Coin(db.Model):
    __table_args__ = (
        db.UniqueConstraint('coin_id', 'added_date','coin_price', name='unique_component_commit'),
    )
    coin_id = db.Column(db.Integer, primary_key=True)  #primary
    coin_name = db.Column(db.String(30))
    added_date = db.Column(db.DateTime, primary_key=True)
    coin_price = db.Column(db.Float, nullable=False)
    coin_price_change_1h = db.Column(db.Float,nullable=False)
    coin_price_change_24h = db.Column(db.Float,nullable = False)
    coin_volume_24h = db.Column(db.Float, nullable=False)
    coin_volume_change_24h = db.Column(db.Float,nullable = False)  
    coin_market_cap = db.Column(db.Float,nullable=False)
    coin_supply = db.Column(db.Float,nullable = False) 



    def __init__(self, id, name, price, price_change_24h,price_change_1h,volume_24h,volume_change_24h,market_cap,supply):
        super(Coin, self).__init__(coin_id=id,
                                   coin_name=name,
                                   coin_price=price,
                                   coin_price_change_1h=price_change_1h,
                                   coin_price_change_24h = price_change_24h,
                                   coin_volume_24h = volume_24h,
                                   coin_volume_change_24h = volume_change_24h,
                                   coin_market_cap = market_cap,
                                   coin_supply = supply,
                                
                                   added_date=datetime.datetime.now()
                                   )


class CoinSchema(ma.Schema):
    class Meta:
        fields = ("coin_id", "coin_name", "added_date", "coin_price", "coin_24h_change","coin_volumen")
        model = Coin