from flask import abort
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_marshmallow import Marshmallow
from flask import request
from flask import jsonify
from flask_cors import CORS
import jwt


app = Flask(__name__)
bcrypt = Bcrypt(app)
ma = Marshmallow(app)
# SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
#     username="moekach",
#     password="yypQr2G7E@3k5jY",
#     hostname="moekach.mysql.pythonanywhere-services.com",
#     databasename="moekach$TradingBot",
# )

SQLALCHEMY_DATABASE_URI = 'postgresql://oswkpkahzgjkiv:c3b16a75277b0ab027d691af498e02311a4bd71d326fbdb5bc44963ecb7b2d63@ec2-99-80-170-190.eu-west-1.compute.amazonaws.com:5432/de3m9bpar6f74q'

app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
# app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
CORS(app)
db = SQLAlchemy(app)


from .models.user import User, UserSchema
# from .models.coin import Coin, CoinSchema

# transaction_schema = CoinSchema()
# transactions_schema = CoinSchema(many=True)



# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_name = db.Column(db.String(30), unique=True)
#     hashed_password = db.Column(db.String(128))

#     def __init__(self, user_name, password):
#         super(User, self).__init__(user_name=user_name)
#         self.hashed_password = bcrypt.generate_password_hash(password)


# class UserSchema(ma.Schema):
#     class Meta:
#         fields = ("id", "user_name")
#         model = User


user_schema = UserSchema()

@app.route('/hello', methods=['GET'])
def hello_world():
    return 'Hello World!'



@app.route('/user', methods=['POST'])
def user():
    user_name = request.json["user_name"]
    password = request.json["password"]
    existingUser = User.query.filter_by(user_name=user_name).first()

    if(existingUser != None):
        return "User Already Exists"
    user_instance = User(user_name, password)
    db.session.add(user_instance)
    db.session.commit()
    return jsonify(user_schema.dump(user_instance))


@app.route('/authentication', methods=['POST'])
def authentication():
    user_name = request.json["user_name"]
    password = request.json["password"]
    if user_name is None or password is None or user_name is "" or password is "":
        abort(400)
    user_instance = User.query.filter_by(user_name=user_name).first()
    # if user_instance is None:
        # abort(403)
    if not bcrypt.check_password_hash(password,user_instance.hashed_password):
        abort(403)
    print(str(user_instance.hashed_password))
    print(str(bcrypt.generate_password_hash(password)))
    return jsonify(user_name = user_name)
