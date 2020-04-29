import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.losses import mse

import pandas as pd
import numpy as np

def predict_reward(hand1, hand2):

    x = np.concatenate([hand1, hand2])
    print(x.shape)
    return model.predict(x.reshape(1, 64))

def decision_process(hand1, hand2):
    max_expected_reward = 0
    final_shift = 0

    for shift in range(0,4):
        shifted_hand1 = shifting_hand(hand1, value=shift)
        shifted_hand2 = shifting_hand(hand2, value=shift)
        predicted_reward = predict_reward(shifted_hand1, shifted_hand2)
        if predicted_reward > max_expected_reward:
            max_expected_reward = predicted_reward
            final_shift = shift
    return final_shift, max_expected_reward
    """
    compute expected reward for all atout_suit and return atout suit and contract value
    
    :param hand1: 
    :param hand2: 
    :return: 
    """

def shifting_hand(hand, value=0):
    return np.roll(hand, value*8) # shifted hand