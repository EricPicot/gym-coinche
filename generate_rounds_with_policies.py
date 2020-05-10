import gym
import numpy as np
import pandas as pd
from coinche.player import AIPlayer, RandomPlayer
from coinche.gym.env import GymPlayer
from tensorflow.keras import models

def policy_competition(policies, env_name = "coinche-v3",
                       contrat_model_path=None, NUM_EPISODES=40000):
    reward_list = []
    player_0_hands = []
    player_1_hands = []
    player_2_hands = []
    player_3_hands = []
    attacker_list = []

    env = gym.make('coinche.gym.env:' + env_name)
    env.__init__()

    for i, p in enumerate(policies):
        if p == "Random":
            if isinstance(env.players[i], GymPlayer):
                local_player = RandomPlayer(i, "N")
            else:
                env.players[i] = RandomPlayer(i, "N")
        else:
            if isinstance(env.players[i], GymPlayer):
                local_player = AIPlayer(p, i, "N")
            else:
                env.players[i] = AIPlayer(p, i, "N")

    env.contrat_model_path = contrat_model_path
    env.contrat_model = models.load_model(env.contrat_model_path) if env.contrat_model_path is not None else None
    for i_episode in range(NUM_EPISODES):
        observation = env.reset()
        total_round_reward = 0

        if i_episode % 500 == 0:
            print(i_episode)

        while True:

            if isinstance(local_player, RandomPlayer):
                action = env.action_space.sample()  # Use a random action
            else:
                action = local_player.get_action(observation.reshape((1, 98)))

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

    hands_and_reward_df = pd.DataFrame(data)

    suit = ["atout", "na1", "na2", "na3"]
    cards = ["7", "8", "9", "10", "jack", "queen", "king", "as"]
    players = ["p1", "p2"]
    players2 = ["p3", "p4"]

    hands_and_reward_df.columns = [(suit * 2)[x // 8] + "_" + cards[x % 8] + "_" + players[x // 32] for x in range(64)] + \
                               [(suit * 2)[x // 8] + "_" + cards[x % 8] + "_" + players2[x // 32] for x in range(64)] + \
                               ["total_reward"]

    attacker_df = pd.DataFrame(attacker_list, columns=["p0", "p1", "p2", "p3"])
    print("Done")
    return hands_and_reward_df, attacker_df



