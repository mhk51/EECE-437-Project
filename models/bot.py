from app import db
from .user import User

class Bot(db.Model):
    bot_id = db.Column(db.Integer,primary_key = True)
    coin_name = db.Column(db.String(30))
    buy_percentage = db.Column(db.Float)
    is_active = db.Column(db.Boolean)
    def __init__(self,bot_id,coin_name):
        super().__init__(bot_id = bot_id,coin_name= coin_name,is_active = False,buy_percentage = 1.0)
    def switch_activate(self):
        self.is_active = not self.is_active
        db.session.commit()
    def buy(self):
        if(self.is_active):
            user_intance = User.query.get(self.bot_id)
            transfer_amount = user_intance.usd_amount*self.buy_percentage
            user_intance.usd_amount -= transfer_amount
            setattr(user_intance,self.coin_name,getattr(user_intance,self.coin_name)+transfer_amount)
            db.session.commit()
    def sell(self):
        if(self.is_active):
            user_intance = User.query.get(self.bot_id)
            coin_amount = getattr(user_intance,self.coin_name)
            transfer_amount = coin_amount*self.buy_percentage
            setattr(user_intance,self.coin_name,coin_amount - transfer_amount)
            user_intance.usd_amount += transfer_amount
            db.session.commit()