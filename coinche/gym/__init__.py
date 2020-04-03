from gym.envs.registration import register

register(
    id='coinche-v0',
    entry_point='coinche.gym.env:GymCoinche',
)
