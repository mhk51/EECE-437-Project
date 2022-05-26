from app import db, bcrypt, ma



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    hashed_password = db.Column(db.String(128))
    dob = db.Column(db.DateTime(128))
    mail = db.Column(db.String(128))
    bitcoin = db.Column(db.Float)
    ethereum = db.Column(db.Float)
    bnb = db.Column(db.Float)
    usd = db.Column(db.Float)

    def __init__(self, username, password, mail, dob):
        super(User, self).__init__(username=username, dob=dob, mail=mail,bitcoin = 0,ethereum = 0,bnb = 0,usd = 100)
        self.hashed_password = bcrypt.generate_password_hash(password)
        


class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "username", "mail", "dob",'bitcoin','ethereum','bnb','usd')
        model = User

user_schema = UserSchema()


