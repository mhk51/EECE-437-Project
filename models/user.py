from ..app import db, bcrypt, ma


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    hashed_password = db.Column(db.String(128))
    dob = db.Column(db.String(128))
    mail = db.Column(db.String(128))
    wallet_id = db.Column(db.Integer, db.ForeignKey('wallet.wallet_id'), nullable=True)

    def __init__(self, username, password, mail, dob):
        super(User, self).__init__(username=username, dob=dob, mail=mail)
        self.hashed_password = bcrypt.generate_password_hash(password)
        # self.wallet_id = 


class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "username", "wallet_id", "mail", "dob")
        model = User
