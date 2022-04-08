from sched import scheduler
from flask import abort
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_marshmallow import Marshmallow
from flask import request
from flask import jsonify
from flask_cors import CORS
import datetime
from datetime import timedelta 
import jwt
from requests import Request,Session
from requests.exceptions import Timeout,TooManyRedirects,ConnectionError
import json
from flask_apscheduler import APScheduler


class Config:
    SCHEDULER_API_ENABLED = True

# create app
app = Flask(__name__)
app.config.from_object(Config())

bcrypt = Bcrypt(app)
ma = Marshmallow(app)
scheduler = APScheduler()
# scheduler.api_enabled = True
scheduler.init_app(app)
scheduler.start()


if __name__ == '__main__':
    app.run()

SQLALCHEMY_DATABASE_URI = 'postgresql://oswkpkahzgjkiv:c3b16a75277b0ab027d691af498e02311a4bd71d326fbdb5bc44963ecb7b2d63@ec2-99-80-170-190.eu-west-1.compute.amazonaws.com:5432/de3m9bpar6f74q'

app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
# app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
CORS(app)
db = SQLAlchemy(app)


from .models.user import User, UserSchema
from .models.coin import Coin, CoinSchema

# transaction_schema = CoinSchema()
# transactions_schema = CoinSchema(many=True)



# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_name = db.Column(db.String(30), unique=True)
#     hashed_password = db.Column(db.String(128))

#     def __init__(self, user_name, password):
#         super(User, self).__init__(user_name=user_name)
#         self.hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')


# class UserSchema(ma.Schema):
#     class Meta:
#         fields = ("id", "user_name")
#         model = User


user_schema = UserSchema()

# class Coin(db.Model):
#     __table_args__ = (
#         db.UniqueConstraint('coin_id', 'added_date','coin_price', name='unique_component_commit'),
#     )
#     coin_id = db.Column(db.Integer, primary_key=True)  #primary
#     coin_name = db.Column(db.String(30))
#     added_date = db.Column(db.DateTime, primary_key=True)
#     coin_price = db.Column(db.Float, nullable=False)
#     coin_price_change_1h = db.Column(db.Float,nullable=False)
#     coin_price_change_24h = db.Column(db.Float,nullable = False)
#     coin_volume_24h = db.Column(db.Float, nullable=False)
#     coin_volume_change_24h = db.Column(db.Float,nullable = False)  
#     coin_market_cap = db.Column(db.Float,nullable=False)
#     coin_supply = db.Column(db.Float,nullable = False) 



#     def __init__(self, id, name, price, price_change_24h,price_change_1h,volume_24h,volume_change_24h,market_cap,supply):
#         super(Coin, self).__init__(coin_id=id,
#                                    coin_name=name,
#                                    coin_price=price,
#                                    coin_price_change_1h=price_change_1h,
#                                    coin_price_change_24h = price_change_24h,
#                                    coin_volume_24h = volume_24h,
#                                    coin_volume_change_24h = volume_change_24h,
#                                    coin_market_cap = market_cap,
#                                    coin_supply = supply,
                                
#                                    added_date=datetime.datetime.now()
#                                    )


# class CoinSchema(ma.Schema):
#     class Meta:
#         fields = ("coin_id", "coin_name", "added_date", "coin_price", "coin_24h_change","coin_volumen")
#         model = Coin


SECRET_KEY = "b'|\xe7\xbfU3`\xc4\xec\xa7\xa9zf:}\xb5\xc7\xb9\x139^3@Dv'"

def create_token(user_id):
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=4),
        'iat': datetime.datetime.utcnow(),
        'sub': user_id
    }
    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm='HS256'
    )


def extract_auth_token(authenticated_request):
    auth_header = authenticated_request.headers.get('Authorization')
    if auth_header:
        return auth_header.split(" ")[1]
    else:
        return None


def decode_token(token):
    payload = jwt.decode(token, SECRET_KEY, 'HS256')
    return payload['sub']



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
    print(user_instance.hashed_password)
    db.session.add(user_instance)
    db.session.commit()
    user_instance2 = User.query.filter_by(user_name=user_name).first()
    print(user_instance2.hashed_password)
    return jsonify(user_schema.dump(user_instance))


@app.route('/authentication', methods=['POST'])
def authentication():
    user_name = request.json["user_name"]
    password = request.json["password"]
    if user_name is None or password is None or user_name is "" or password is "":
        abort(400)
    user_instance = User.query.filter_by(user_name=user_name).first()
    if user_instance is None:
        abort(403)
    if not bcrypt.check_password_hash(user_instance.hashed_password,password):
        abort(403)
    tkn = create_token(user_instance.id)
    return jsonify(token=tkn)


@scheduler.task('interval',id='getCryptoPrices',seconds = 30)
def getCryptoPrices():
    with scheduler.app.app_context():
        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
        headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': 'd00bc3fb-616a-40fa-8cba-14ce888e5c70',
        }
        session = Session()
        session.headers.update(headers)

        try:
            response = session.get(url)
            data = json.loads(response.text)
            data = data['data']
            # with open('test.json', 'w') as outfile:
            #     json.dump(data, outfile,indent=4)
            for index in range(0,6):
                if(index == 2 or index == 4): #skipping USDT and USD-C
                    continue
                coin = data[index]
                id = coin['id']
                name = coin['name']
                coinData = coin['quote']['USD']
                price = coinData['price']
                price_change_1h = coinData['percent_change_1h'],
                price_change_24h = coinData['percent_change_24h'],
                volume_24h = coinData['volume_24h'],
                volume_change_24h = coinData['volume_change_24h'],
                market_cap = coinData['market_cap'],
                supply = coin['circulating_supply'],
                coin_instance = Coin(id,name,price,price_change_24h,price_change_1h,volume_24h,volume_change_24h,market_cap,supply)
                print(coin_instance)
                db.session.add(coin_instance)
                db.session.commit()
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)
        return jsonify(message = 'success')


@app.route('/getTrend',methods = ['GET'])
def getTrend():
    coinList = Coin.query.all()
    dictionary = {}
    for coin in coinList:
        if(coin.coin_name not in dictionary):
            dictionary[coin.coin_name] = [{'price':coin.coin_price,'date':coin.added_date}]
        else:
            dictionary[coin.coin_name].append({'price':coin.coin_price,'date':coin.added_date})
        print(coin.coin_name,coin.coin_price,coin.added_date)
    return jsonify(dictionary)

