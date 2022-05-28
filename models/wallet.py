from app import db, ma


class Wallet(db.Model):
    wallet_id = db.Column(db.Integer,db.ForeignKey('user.id'), primary_key=True)
    bitcoin = db.Column(db.Float)
    ethereum = db.Column(db.Float)
    bnb = db.Column(db.Float)
    usd = db.Column(db.Float)


    def __init__(self):
        super().__init__(usd=100,bitcoin=0,bnb=0,ethereum=0)


class WalletSchema(ma.Schema):
    class Meta:
        fields = ("wallet_id","user_id","bitcoin","ethereum","bnb","usd")
        model = Wallet