from gym.envs.registration import register
from coinche.player import RandomPlayer, AIPlayer
from coinche.gym.player import GymPlayer

register(
    id='coinche-v0',
    entry_point='coinche.gym.env:GymCoinche'
)

register(
    id='coinche-v1',
    entry_point='coinche.gym.env:GymCoinche',
    kwargs={'players': [
            AIPlayer("./experiments/coinche/07_05_2020-14_22/checkpoint/0_Step-354.ckpt", 0, "N"),
            RandomPlayer(1, "E"),
            GymPlayer(2, "S"),
            RandomPlayer(3, "W")
            ]}
)
