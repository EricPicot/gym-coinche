import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

data = pd.read_csv('data/hands_and_reward.csv')
data = data.drop("Unnamed: 0", axis=1)

# # To run if you created hands_and_reward_full_ai.csv that is obtained using 4 AIPlayers int env.py
# data_full_ai = pd.read_csv('data/hands_and_reward_full_ai.csv')
# data_full_ai = data_full_ai.drop("Unnamed: 0", axis=1)


plt.hist(data["64"], bins=np.arange(10, 170, 5), label="3 random + 1 AI")
# # To run if you created hands_and_reward_full_ai.csv that is obtained using 4 AIPlayers int env.py
# plt.hist(data_full_ai["64"],  bins= np.arange(10, 170, 5), label="4 AI")
plt.title(" Impact of sampling on random total reward")
plt.legend()
plt.show()
