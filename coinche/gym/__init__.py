from gym.envs.registration import register
from coinche.player import RandomPlayer, AIPlayer
from coinche.gym.player import GymPlayer
import os
print(os.listdir())

#
# register(
#     id='coinche-v0',
#     entry_point='coinche.gym.env:GymCoinche'
# )
#
register(
    id='coinche-v1',
    entry_point='coinche.gym.env:GymCoinche',
    kwargs={
        'players': [
            RandomPlayer(0, "N"),
            RandomPlayer(1, "E"),
            GymPlayer(2, "S"),
            RandomPlayer(3, "W")
        ],
        'contrat_model_path': './reward_prediction/reward_model.h5'
    }
)
#
# register(
#     id='coinche-v2',
#     entry_point='coinche.gym.env:GymCoinche',
#     kwargs={
#         'players': [
#             AIPlayer("./experiments/coinche/08_05_2020-16_10/checkpoint/1_Step-434.ckpt", 0, "N"),
#             RandomPlayer(1, "E"),
#             GymPlayer(2, "S"),
#             RandomPlayer(3, "W")
#         ],
#         'contrat_model_path': './reward_prediction/reward_model.h5'
#     }
# )

register(
    id='coinche-v3',
    entry_point='coinche.gym.env:GymCoinche',
    kwargs={
        'players': [
            RandomPlayer(0, "N"),
            RandomPlayer(1, "E"),
            GymPlayer(2, "S"),
            RandomPlayer(3, "W"),
        ],
    }
)

register(
    id='coinche-v4',
    entry_point='coinche.gym.env:GymCoinche',
    kwargs={
        'players': [
            AIPlayer("./experiments/coinche/09_05_2020-15_13/checkpoint/311_Step-79961.ckpt", 0, "N"),
            AIPlayer("./experiments/coinche/09_05_2020-15_13/checkpoint/311_Step-79961.ckpt", 1, "E"),
            GymPlayer(2, "S"),
            AIPlayer("./experiments/coinche/09_05_2020-15_13/checkpoint/311_Step-79961.ckpt", 3, "W")
        ],
        'contrat_model_path': './reward_prediction/reward_model.h5'
    }
)
