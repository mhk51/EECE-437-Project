from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="moekach",
    password="yypQr2G7E@3k5jY",
    hostname="moekach.mysql.pythonanywhere-services.com",
    databasename="moekach$TradingBot",
)

@app.route('/hello', methods=['GET'])
def hello_world():
    return 'Hello World!'
