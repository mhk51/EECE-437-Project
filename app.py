from sched import scheduler
from flask import abort, render_template, session
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_marshmallow import Marshmallow
from flask import request
from flask import jsonify
from flask_cors import CORS
import datetime
from flask_cors import CORS, cross_origin
from datetime import timedelta
import jwt
from requests import Request, Session
from requests.exceptions import Timeout, TooManyRedirects, ConnectionError
import json
from flask_apscheduler import APScheduler
from flask_mail import Mail, Message
from db_config import SQLALCHEMY_DATABASE_URI

# class Config:
    # SCHEDULER_API_ENABLED = True


# create app
app = Flask(__name__)
app.secret_key = "super secret key"
# app.config.from_object(Config())

bcrypt = Bcrypt(app)
ma = Marshmallow(app)
scheduler = APScheduler()
scheduler.api_enabled = True
scheduler.init_app(app)
# scheduler.start()

if __name__ == '__main__':
    app.run()

# SQLALCHEMY_DATABASE_URI = 'postgresql://oswkpkahzgjkiv:c3b16a75277b0ab027d691af498e02311a4bd71d326fbdb5bc44963ecb7b2d63@ec2-99-80-170-190.eu-west-1.compute.amazonaws.com:5432/de3m9bpar6f74q'


app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
# app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
CORS(app)
db = SQLAlchemy(app)
Email = Mail(app)

from models.user import User, UserSchema
from models.coin import Coin, CoinSchema
from models.bot import Bot


# transaction_schema = CoinSchema()
# transactions_schema = CoinSchema(many=True)




user_schema = UserSchema()


@app.route('/Sign_in.html')
def init():
    return render_template('Sign_in.html')


@app.route('/Sign_up.html')
def index():
    return render_template('Sign_up.html')


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



@scheduler.task('interval', id='getCryptoPrices', seconds=5)
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
            for index in range(0, 4):
                if (index == 2):  # skipping USDT and USD-C
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
                coin_instance = Coin(id, name, price, price_change_24h, price_change_1h, volume_24h, volume_change_24h,
                                     market_cap, supply)
                print(coin_instance)
                db.session.add(coin_instance)
                db.session.commit()
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)
        return jsonify(message='success')


@app.route('/getTrend', methods=['GET'])
def getTrend():
    coinList = Coin.query.all()
    dictionary = {}
    for coin in coinList:
        if (coin.coin_name not in dictionary):
            dictionary[coin.coin_name] = [{'price': coin.coin_price, 'date': coin.added_date}]
        else:
            dictionary[coin.coin_name].append({'price': coin.coin_price, 'date': coin.added_date})
        print(coin.coin_name, coin.coin_price, coin.added_date)
    return jsonify(dictionary)


@app.route('/add_user', methods=['POST'])
@cross_origin(supports_credentials=True)
def add_user():
    name = request.json['username']
    pwd = request.json['password']
    mail = request.json['mail']
    dob = request.json['dob']
    if not name or not pwd or not dob or not mail:
        # name is empty or pwd is empty
        abort(400)
    # check for unique name
    not_unique = User.query.filter_by(username=name).first()
    # similar username exists
    if not_unique:
        abort(403)
    else:
        newuser = User(name, pwd, mail, dob)
        bot_instance = Bot(newuser.id,'bitcoin_amount')
        db.session.add(bot_instance)
        db.session.commit()
        db.session.add(newuser)
        db.session.commit()
        sender = 'terkiz.club@gmail.com'
        recipients = [mail]
        subject ="Welcome to Mokash Trading Bot"
        msg = Message(subject, sender=sender, recipients=recipients)
        msg.body = "Thank you for joining Mokash Trading Bot, " + name+ " \n We hope that you will like it here! \n Feel free to look through the site. \n Best,\n MoKash Trading Team. "
        # Email.send(msg)

        return jsonify(user_schema.dump(newuser))


@app.route('/authentication', methods=['POST'])
def authenticate():
    usname = request.json['username']
    pwd = request.json['password']
    if not id or not pwd:
        abort(400)
    user_db = User.query.filter_by(username=usname).first()
    # no username exists
    if user_db is None:
        abort(403)
    # password don't match
    if not bcrypt.check_password_hash(user_db.hashed_password, pwd):
        abort(403)
    # create token
    token = create_token(user_db.id)
    session["id"] = user_db.id
    session.modified = True
    return jsonify({"token": token})


@app.route('/makeTransaction',methods = ['GET'])
def makeTransaction():
    id = session['id']
    bot_intance = Bot.query.filter_by(bot_id = id).first()
    bot_intance.sell()
    return 'success'

@app.route('/activateBot',methods = ['GET'])
def activateBot():
    id = session['id']
    bot_intance = Bot.query.get(id)
    bot_intance.activate()
    return 'success'