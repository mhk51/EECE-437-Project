from email import header
import json
import math
from sched import scheduler
from xmlrpc.client import DateTime
from flask import abort, render_template, session
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_marshmallow import Marshmallow
from flask import request
from flask import jsonify
from flask_cors import CORS
import datetime
from dateutil import parser
from flask_cors import CORS, cross_origin
import jwt
from requests.exceptions import Timeout, TooManyRedirects, ConnectionError
from flask_apscheduler import APScheduler
from flask_mail import Mail, Message
from Bot import CoinPrediction
import requests
import pandas as pd
import numpy as np
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
scheduler.start()

if __name__ == '__main__':
    app.run(debug=True)

# SQLALCHEMY_DATABASE_URI = 'postgresql://oswkpkahzgjkiv:c3b16a75277b0ab027d691af498e02311a4bd71d326fbdb5bc44963ecb7b2d63@ec2-99-80-170-190.eu-west-1.compute.amazonaws.com:5432/de3m9bpar6f74q'


app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
# app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
CORS(app)
db = SQLAlchemy(app)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'remextrading3@gmail.com'
app.config['MAIL_PASSWORD'] = 'remexTrading@3'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
Email = Mail(app)

from models.user import User, UserSchema
from models.coin import Coin, CoinSchema
from models.bot import Bot,BotSchema
from models.transaction import Transaction,TransactionSchema
from models.wallet import Wallet,WalletSchema



model = CoinPrediction('model.json','model_weights.h5')

transactions_schema = TransactionSchema(many=True)
coins_schema = CoinSchema(many=True)
user_schema = UserSchema()
bot_schema = BotSchema()
wallet_schema = WalletSchema()


@app.route('/Sign_in.html',methods = ['GET','POST'])
def init():
    if(request.method == 'POST'):
        print(request.form['username'])
        print(request.form['password'])
    return render_template('Sign_in.html')


@app.route('/Sign_up.html',methods = ['GET','POST'])
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



@scheduler.task('interval', id='get_crypto_prices', minutes=30)
def get_crypto_prices():
    with scheduler.app.app_context():
        url_btc = 'https://rest.coinapi.io/v1/ohlcv/BITSTAMP_SPOT_BTC_USD/latest?period_id=1HRS&limit=200'
        headers_btc = {
            'X-CoinAPI-Key': '7F5B67D5-EE33-4B3D-924D-3E2384904663',
        }
        url_eth = 'https://rest.coinapi.io/v1/ohlcv/BITSTAMP_SPOT_ETH_USD/latest?period_id=1HRS&limit=200'
        headers_eth = {
            'X-CoinAPI-Key': '1F18A075-8090-4F2E-9AF1-94D22E9E7A2F',
        }
        try:
            response_btc = requests.get(url_btc, headers=headers_btc)
            json_btc = response_btc.json()
            
            df_btc = pd.DataFrame(json_btc)
            # df_btc = pd.read_json("data.json")
            df_btc = df_btc[['time_period_start','price_open','price_high','price_low','price_close','volume_traded']]
            for i in range(df_btc.shape[0]):
                row = df_btc.iloc[i]
                date = parser.parse(row['time_period_start'])
                coin_instance = Coin("Bitcoin",row['price_open'],row['price_high'],row['price_low'],row['price_close'],row['volume_traded'],date)
                db.session.merge(coin_instance)
            df_btc = df_btc.drop('time_period_start',axis=1).pct_change().dropna()
            input_data = df_btc.iloc[0:5].values
            sigmoid = model.predict_coin(np.array([input_data]))
            inverse_sigmoid = -math.log((1-sigmoid)/sigmoid)
            confidence_btc = (math.tanh(inverse_sigmoid))
            exchangeRates = exchange()

            response_eth = requests.get(url_eth,headers=headers_eth)
            json_eth = response_eth.json()  
            df_eth = pd.DataFrame(json_eth)
            # df_eth = pd.read_json("data.json")
            df_eth = df_eth[['time_period_start','price_open','price_high','price_low','price_close','volume_traded']]
            for i in range(df_eth.shape[0]):
                row = df_eth.iloc[i]
                date = parser.parse(row['time_period_start'])
                coin_instance = Coin("Ethereum",row['price_open'],row['price_high'],row['price_low'],row['price_close'],row['volume_traded'],date)
                db.session.merge(coin_instance)
            df_eth = df_eth.drop('time_period_start',axis=1).pct_change().dropna()
            input_data = df_eth.iloc[0:5].values
            sigmoid = model.predict_coin(np.array([input_data]))
            inverse_sigmoid = -math.log((1-sigmoid)/sigmoid)
            confidence_eth = (math.tanh(inverse_sigmoid))

            bots = Bot.query.all()
            for bot in bots:
                if(bot.coin_name == 'bitcoin'):
                    bot.make_trade(confidence_btc,exchangeRates)
                elif bot.coin_name == 'ethereum' :
                    bot.make_trade(confidence_eth,exchangeRates)


        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)


        db.session.commit()
        return jsonify(message='success')

def exchange():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': 'd00bc3fb-616a-40fa-8cba-14ce888e5c70',
    }
    response = requests.get(url,headers=headers)
    json_object = response.json()
    bitcoin =  json_object['data'][0]
    ethereum = json_object['data'][1]
    data = {
            'bitcoin':bitcoin['quote']['USD']['price'],
            'ethereum':ethereum['quote']['USD']['price']
    }
    return data

def wallet_total(user_id):
    wallet_instance = Wallet.query.get(user_id)
    data = exchange()
    bitcoin_amount = wallet_instance.bitcoin*data['bitcoin']
    ethereum_amount = wallet_instance.ethereum*data['ethereum']
    usd_amount = wallet_instance.usd
    return bitcoin_amount+ethereum_amount+usd_amount


@app.route('/trend', methods=['POST'])
def get_trend():
    coin_name = request.json['coin_name']
    hours = request.json['hours']
    end_date = datetime.datetime.now()
    start_date = datetime.datetime.now() - datetime.timedelta(hours=hours)
    coinList  = Coin.query.filter(Coin.date.between(start_date, end_date)).filter_by(coin_name=coin_name).all()
    return jsonify(coins_schema.dump(coinList))


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
        wallet_instance = Wallet()
        bot_instance = Bot('bitcoin')
        newuser.wallet = wallet_instance
        newuser.bot = bot_instance
        db.session.add(newuser)
        db.session.commit()
        sender = 'terkiz.club@gmail.com'
        recipients = [mail]
        subject ="Welcome to Moekash Trading Bot"
        msg = Message(subject, sender=sender, recipients=recipients)
        msg.body = "Thank you for joining Moekash Trading Bot, " + name+ " \n We hope that you will like it here! \n Feel free to look through the site. \n Best,\n MoKash Trading Team. "
        Email.send(msg)

        return jsonify(user_schema.dump(newuser))


@app.route('/authentication', methods=['POST'])
def authenticate():
    usname = request.json['username']
    pwd = request.json['password']
    if not id or not pwd:
        abort(400)
    user_db = User.query.filter_by(username=usname).first()
    if user_db is None:
        abort(403)
    if not bcrypt.check_password_hash(user_db.hashed_password, pwd):
        abort(403)
    token = create_token(user_db.id)
    return jsonify({"token": token})

@app.route('/transactions',methods=['GET'])
def transactions():
    tkn = extract_auth_token(request)
    if tkn is not None:
        try:
            user_id = decode_token(tkn)
        except jwt.exceptions.InvalidSignatureError:
            abort(403)
    else:
        abort(403)
    transactions = Transaction.query.filter_by(user_id=user_id).all()
    return jsonify(transactions_schema.dump(transactions))

@app.route('/switchActivate',methods = ['GET'])
def switchActivate():
    tkn = extract_auth_token(request)
    if tkn is not None:
        try:
            user_id = decode_token(tkn)
        except jwt.exceptions.InvalidSignatureError:
            abort(403)
    else:
        abort(403)
    bot_intance = Bot.query.get(user_id)
    bot_intance.switch_activate()
    return jsonify(bot_schema.dump(bot_intance))


@app.route('/buy',methods = ['POST'])
def buy():
    tkn = extract_auth_token(request)
    if tkn is not None:
        try:
            user_id = decode_token(tkn)
        except jwt.exceptions.InvalidSignatureError:
            abort(403)
    else:
        abort(403)
    bot_instance = Bot.query.get(user_id)
    bot_instance.make_trade(request.json['confidence'],request.json['data'])
    return 'success'


@app.route('/change_param',methods = ['POST'])
def changeParams():
    tkn = extract_auth_token(request)
    if tkn is not None:
        try:
            user_id = decode_token(tkn)
        except jwt.exceptions.InvalidSignatureError:
            abort(403)
    else:
        abort(403)
    coin_name = request.json['coin_name']
    buy_percentage = request.json['buy_percentage']
    risk = request.json['risk']
    bot_instance = Bot.query.get(user_id)
    bot_instance.changeParams(risk,buy_percentage,coin_name)
    return jsonify(bot_schema.dump(bot_instance))



@app.route('/bot',methods = ['GET'])
def bot():
    tkn = extract_auth_token(request)
    if tkn is not None:
        try:
            user_id = decode_token(tkn)
        except jwt.exceptions.InvalidSignatureError:
            abort(403)
    else:
        abort(403)
    bot_instance = Bot.query.get(user_id)
    return jsonify(bot_schema.dump(bot_instance))



@app.route('/performance',methods = ['POST'])
def performance():
    tkn = extract_auth_token(request)
    if tkn is not None:
        try:
            user_id = decode_token(tkn)
        except jwt.exceptions.InvalidSignatureError:
            abort(403)
    else:
        abort(403)
    days = request.json['days']
    list = []
    end_date = datetime.datetime.now()
    start_date = datetime.datetime.now() - datetime.timedelta(days=days)
    transactions  = Transaction.query.filter(Transaction.date.between(start_date, end_date)).all()
    for tx in transactions:
        list.append({'id':tx.id,'date':tx.date,'amount':tx.user_total})
    list.append({'id':tx.id+1,'date':datetime.datetime.now(),'amount':wallet_total(user_id)})
    return jsonify(list)



@app.route('/wallet',methods=['GET'])
def wallet():
    tkn = extract_auth_token(request)
    if tkn is not None:
        try:
            user_id = decode_token(tkn)
        except jwt.exceptions.InvalidSignatureError:
            abort(403)
    else:
        abort(403)
    wallet_instance = Wallet.query.get(user_id)
    return jsonify(wallet_schema.dump(wallet_instance))


@app.route('/exchangeRate',methods=['GET'])
def exchangeRate():
    return exchange()