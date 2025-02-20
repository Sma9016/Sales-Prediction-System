import numpy as np
import math
import pandas as pd
import pickle
model=pickle.load(open('model.pkl','rb'))

def predict(values):
    values=np.array(values)
    new_val=values.reshape(1,19)
    result=model.predict(new_val)
    return result