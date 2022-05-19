from tensorflow.keras.models import model_from_json

import numpy as np

class CoinPrediction(object):
    def __init__(self,model_json_file,model_weights_file):
        with open(model_json_file,"r") as json_file:
            loaded_model_json = json_file.read()
        self.loaded_model = model_from_json(loaded_model_json)
        self.loaded_model.load_weights(model_weights_file)
        self.loaded_model.make_predict_function()
    def predict_coin(self,data):
        return self.loaded_model.predict(data)[0][0]

model = CoinPrediction('model.json','model_weights.h5')

# list =[
#         [
#             [-0.00156848,-0.00436584,-0.00928349,0.00222321,0.02287013],
#             [-0.00217508,-0.00137908,0.00301958,-0.00216624,-0.17925166],
#             [-0.00555814,-0.0026993,-0.00637157,-0.00197996,-0.09231805],
#             [-0.00220383,-0.00643296,-0.00250089,-0.00583801,-0.33689167],
#             [-0.0039981,0.00565537,0.00414033,-0.00092567,0.27576782]
#         ],
#     ]
# print(model.predict_coin(list))

