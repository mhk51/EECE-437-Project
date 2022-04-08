from ..app import db, bcrypt, ma


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(30), unique=True)
    hashed_password = db.Column(db.String(128))
    wallet_id = db.Column(db.Integer, db.ForeignKey('wallet.wallet_id'), nullable=True)

    def __init__(self, user_name, password):
        super(User, self).__init__(user_name=user_name)
        self.hashed_password = bcrypt.generate_password_hash(password)
        # self.wallet_id = 


class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "user_name", "wallet_id")
        model = User