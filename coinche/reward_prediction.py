from tensorflow.keras import layers, models
import numpy as np
import random


model = models.load_model("./reward_prediction/reward_model.h5")

def predict_reward(hand1, hand2):

    x = np.concatenate([hand1, hand2])
    return model.predict(x.reshape(1, 64))


def shifting_hand(hand, value=0):
    return np.roll(hand, value*8) # shifted hand


def decision_process(hand1, hand2):
    max_expected_reward = 0
    final_shift = None

    for shift in range(0,4):
        shifted_hand1 = shifting_hand(hand1, value=shift)
        shifted_hand2 = shifting_hand(hand2, value=shift)
        predicted_reward = predict_reward(shifted_hand1, shifted_hand2)
        if predicted_reward > max_expected_reward:
            max_expected_reward = predicted_reward
            final_shift = shift

    return final_shift, max_expected_reward
