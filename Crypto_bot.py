import pandas as pd
import matplotlib

class user:
    username=''
    password=''
    coins=0
    def __init__(self,usern,pwd):
        self.username=usern
        self.password=pwd
    def sign_up():
        return
    def log_in(usern, pwd):
        #check for availability of username and constraints on the pwd
        user(usern,pwd)
        return

class trend:
    def print_trend():
        data = pd.read_csv(r'')    
        # casting Month column to datetime object
        data['Month'] = pd.to_datetime(data['Month'])
        # Setting Month as index
        data = data.set_index('Month')
        data['2000':'2022'].plot()



class trade:
    coins=0
    amount_paid=0
    trade_id=0
    def print_receipt():
        return
    def is_successfull():
        return
    def confirm():
        return


class cryptocurr:
    trend
    value=0
    def print_trend():
        return
    def get_value(self):
        return self.value
    

class Crypto_bot:
    trend
    user
    cryptocurr
    def activate(self):
        #on start this function will be called
        return
    def deactivate(self):
        #on stop this fucntion will be called
        return
    def predict_price(cryptocurr):
        return
    def sell_coin(user, cryptocurr):
        return
    def buy_coin(user, cryptocurr):
        return
    def adjust_exposure(user, trade):
        return
    def trend_train(trend):
        return