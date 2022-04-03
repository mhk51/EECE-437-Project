from ..app import db, bcrypt, ma


class Coin(db.Model):
    __table_args__ = (
        db.UniqueConstraint('coin_id', 'coin_name', name='unique_component_commit'),
    )
    coin_id = db.Column(db.Integer, primary_key=True)  #primary
    coin_name = db.Column(db.String(30))
    coin_price = db.Column(db.Float)  
    coin_date = db.Column(db.date)    #primary key
    
    def __init__(self, id, name):
        super(Coin, self).__init__(coin_id = id,coin_name = name)


class CoinSchema(ma.Schema):
    class Meta:
        fields = ("coin_id", "coin_name")
        model = Coin