import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.losses import mse

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split as tts


data = pd.read_csv('data/random_data.csv', index_col=0)

# Creating class_weigth dict to penalize extreme values
# thresholds = [30, 50, 80, 100, 110]
class_weights = {}
for i in range(163):
    i = float(i)
    if (i <= 40) | (i > 120):
        class_weights[i] = 2.2
    elif (i <= 60) | (i > 100):
        class_weights[i] = 1.8
    elif (i > 90) | (i <70):
        class_weights[i] = 1.3
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

p1_p3 = [x for x in range(0, 32) ]+ [x for x in range(64, 64 + 32)]

xtrain, xtest, ytrain, ytest = tts(data[data.columns[p1_p3]].values, data.total_reward, test_size=0.2, random_state=4)
xtrain = xtrain.reshape((xtrain.shape[0], xtrain.shape[1], 1))
xtest = xtest.reshape((xtest.shape[0], xtest.shape[1], 1))

epochs=18
relu_class_weigth_model.fit(x = xtrain.reshape(xtrain.shape[0], 64), y = ytrain,  epochs=epochs,
                            validation_data=(xtest.reshape(xtest.shape[0], 64), ytest),
                            batch_size=256, class_weight=class_weights)

models.save_model(relu_class_weigth_model, "./reward_model.h5")
