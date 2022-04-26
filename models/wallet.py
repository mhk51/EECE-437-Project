from app import db, bcrypt, ma


class Wallet(db.Model):
    wallet_id = db.Column(db.Integer, primary_key=True)

    def __init__(self, user_name, password):
        super(Wallet, self).__init__(user_name=user_name)
        self.hashed_password = bcrypt.generate_password_hash(password)
        #self.wallet_id =


class WalletSchema(ma.Schema):
    class Meta:
        fields = ("id", "user_name", "wallet_id")
        model = Wallet