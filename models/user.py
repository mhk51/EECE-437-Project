from app import db, bcrypt, ma



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    hashed_password = db.Column(db.String(128))
    dob = db.Column(db.String(128))
    mail = db.Column(db.String(128))
    bitcoin_amount = db.Column(db.Float)
    ethereum_amount = db.Column(db.Float)
    bnb_amount = db.Column(db.Float)
    usd_amount = db.Column(db.Float)

    def __init__(self, username, password, mail, dob):
        super(User, self).__init__(username=username, dob=dob, mail=mail,bitcoin_amount = 0,ethereum_amount = 0,bnb_amount = 0,usd_amount = 100)
        self.hashed_password = bcrypt.generate_password_hash(password)
        


class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "username", "mail", "dob",'bitcoin_amount','ethereum_amount','bnb_amount','usd_amount')
        model = User



user_schema = UserSchema()