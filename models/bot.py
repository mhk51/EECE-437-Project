import requests
from app import db,ma
from .user import User
from .transaction import Transaction

class Bot(db.Model):
    bot_id = db.Column(db.Integer,primary_key = True)
    coin_name = db.Column(db.String(30))
    buy_percentage = db.Column(db.Float)
    is_active = db.Column(db.Boolean)
    risk = db.Column(db.Float)
    bought = db.Column(db.Boolean)
    def __init__(self,bot_id,coin_name):
        super().__init__(bot_id = bot_id,coin_name= coin_name,is_active = False,buy_percentage = 1.0,risk=0.5,bought = False)
    def switch_activate(self):
        self.is_active = not self.is_active
        db.session.commit()
    def changeParams(self,risk,percentage,coin_name):
        if(percentage != 0):
            self.buy_percentage = percentage
        if(risk != 0):
            self.risk = risk
        self.coin_name = coin_name
        db.session.commit()
    def make_trade(self,confidence,data):
        if(confidence < 0):
            if(abs(confidence) > self.risk):
                self.__sell(data)
        else:
            if(abs(confidence) > 1-self.risk):
                self.__buy(data)
    def __buy(self,data):
        if self.is_active and not self.bought:
            user_instance = User.query.get(self.bot_id)
            transfer_amount = user_instance.usd*self.buy_percentage
            user_instance.usd -= transfer_amount
            usd_amount = transfer_amount
            exchangeRate = data[self.coin_name]
            coin_amount = transfer_amount/exchangeRate
            setattr(user_instance,self.coin_name,getattr(user_instance,self.coin_name)+coin_amount)
            self.bought = True
            tx_instance = Transaction(self.bot_id,exchangeRate,True,self.coin_name,coin_amount,usd_amount,usd_amount+coin_amount*exchangeRate-transfer_amount)
            db.session.add(tx_instance)
            db.session.commit()
    def __sell(self,data):
        if self.is_active and self.bought:
            user_instance = User.query.get(self.bot_id)
            coin_amount = getattr(user_instance,self.coin_name)
            exchangeRate = data[self.coin_name]
            usd_amount = exchangeRate * coin_amount
            setattr(user_instance,self.coin_name,0)
            user_instance.usd += usd_amount
            self.bought = False
            tx_instance = Transaction(self.bot_id,exchangeRate,False,self.coin_name,coin_amount,usd_amount,usd_amount)
            db.session.add(tx_instance)
            db.session.commit()

    

class BotSchema(ma.Schema):
    class Meta:
        fields = ("bot_id", "coin_name",'buy_percentage','is_active','risk','bought')
        model = Bot