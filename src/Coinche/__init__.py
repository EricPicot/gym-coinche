from .Coinche import *

from gym.envs.registration import register

register(
    id='Coinche_Game-v0',
    entry_point='Coinche.Coinche:CoincheEnv',
    kwargs={'playersName': ['Nord', 'Est', 'Sud', 'Ouest'], 'maxScore': 1000}
)