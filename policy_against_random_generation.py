import gym
import numpy as np
import pandas as pd
import os
from coinche.player import AIPlayer
reward_list = []
player_0_hands = []
player_1_hands = []
player_2_hands = []
player_3_hands = []
attacker_list = []
NUM_EPISODES = 1000

policy_algo = ["experiments/coinche/08_05_2020-16_10/checkpoint/0_Step-81.ckpt",
               "experiments/coinche/08_05_2020-16_10/checkpoint/1_Step-434.ckpt"]


env = gym.make('coinche.gym.env:coinche-v3')

env.players[0] = AIPlayer(policy_algo[0], 0, "N")
env.players[1] = AIPlayer(policy_algo[1], 1, "E")
local_player = AIPlayer(policy_algo[0], 2, 'S')
env.players[3] = AIPlayer(policy_algo[1], 3, "W")
env.contrat_model_path = "reward_prediction/reward_model.h5"
env.__init__()

for i_episode in range(NUM_EPISODES):
    observation = env.reset()
    total_round_reward = 0

    if i_episode % 500 == 0:
        print(i_episode)

    while True:
        # try:
        action = local_player.get_action(observation.reshape((1,98)))
        # action = env.action_space.sample()  # Use a random action
        observation, reward, done, info = env.step(action)  # to take a single step in the environment
        total_round_reward += reward
        if done:
            reward_list.append(total_round_reward)
            player_0_hands.append(info["player0-hand"])
            player_1_hands.append(info["player1-hand"])
            player_2_hands.append(info["player2-hand"])
            player_3_hands.append(info["player3-hand"])
            attacker_list.append(info["attacker_team"])
            break

    env.close()  # Close the environment

player_0_hands = np.array(player_0_hands)
player_1_hands = np.array(player_1_hands)
player_2_hands = np.array(player_2_hands)
player_3_hands = np.array(player_3_hands)
reward_list = np.array(reward_list).reshape((len(reward_list), 1))

data = np.concatenate([player_0_hands, player_1_hands,
                       player_2_hands, player_3_hands, reward_list],
                      axis=1)

df = pd.DataFrame(data)
df.to_csv("reward_prediction/data/competition_hands_and_reward.csv")

pd.DataFrame(attacker_list, columns=["p0", "p1", "p2", "p3"])\
    .to_csv("reward_prediction/data/competition_attacker_teams.csv")
print("Done")
