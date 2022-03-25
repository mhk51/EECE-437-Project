from ..app import db, bcrypt, ma


class Coin(db.Model):
    coin_id = db.Column(db.Integer, primary_key=True)
    coin_name = db.Column(db.String(30), unique=True)

    def __init__(self, id, name):
        super(Coin, self).__init__(coin_id = id,coin_name = name)


class CoinSchema(ma.Schema):
    class Meta:
        fields = ("coin_id", "coin_name")
        model = Coin