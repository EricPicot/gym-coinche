from tensorflow.keras import layers, models

import numpy as np
import random


model = models.load_model("../reward_prediction/reward_model.h5")

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
def set_contrat(players):

    shift_team1, expected_reward_team1 = decision_process(players[0].cards, players[2].cards)
    shift_team2, expected_reward_team2 = decision_process(players[1].cards, players[3].cards)

    if expected_reward_team1 > expected_reward_team2:
        expected_reward_team = expected_reward_team1
        attacker_team = 0
        shift = shift_team1
    else:
        expected_reward_team = expected_reward_team2
        attacker_team = 1
        shift = shift_team2

    for p in players:
        p.cards = shifting_hand(p.cards, value=shift)

    value = random.randint(0, 9) / 9  # Can only announce 80 or 90 to begin with

    attacker_team = random.randint(0, 1)  # 0 if it is team 0 (player 0 and player 2) else 1 for team 1

    return attacker_team, value


def shifting_hand(hand, value=0):
    return np.roll(hand, value*8) # shifted hand