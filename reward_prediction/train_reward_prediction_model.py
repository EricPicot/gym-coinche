import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.losses import mse

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split as tts


data = pd.read_csv('data/random_hands_and_reward.csv')
data = data.drop("Unnamed: 0", axis=1)

suit = ["atout", "na_1", "na_2", "na_3"]
cards = ["7", "8", "9", "10", "jack", "queen", "king", "as"]
players = ["p1", "p2"]
data.columns = [(suit*2)[x//8]+"_"+cards[x%8]+"_"+players[x//32] for x in range(64)] + ["total_reward"]

# Import model
class_weights = {}
for i in range(163):
    i = float(i)
    if i > 110:
        class_weights[i] = 4
    elif (i <= 50) | (i > 100):
        class_weights[i] = 3
    elif (i > 82) | (i <60):
        class_weights[i] = 2
    else:
        class_weights[i] = 1


def build_model():
    model = models.Sequential()
    model.add(layers.Dense(256, activation='relu', input_shape=(64,)))
    model.add(layers.Dense(64, activation='relu'))
    model.add(layers.Dense(32, activation='relu'))
    model.add(layers.Dense(8, activation='relu'))
    model.add(layers.Dense(1))
    return model

relu_class_weigth_model = build_model()
loss = mse
relu_class_weigth_model.compile(optimizer="adam", loss=loss)


xtrain, xtest, ytrain, ytest = tts(data[data.columns[:-1]].values, data.total_reward, test_size=0.2, random_state=4)
xtrain = xtrain.reshape((xtrain.shape[0], xtrain.shape[1], 1))
xtest = xtest.reshape((xtest.shape[0], xtest.shape[1], 1))

epochs=50
relu_class_weigth_model.fit(x = xtrain.reshape(xtrain.shape[0], 64), y = ytrain, epochs=epochs, batch_size=256, class_weight=class_weights)

models.save_model(relu_class_weigth_model, "./reward_model.h5")
