# Coinche R.O.

Coinche is a game card.

[Here](https://ibelote.com/en/rules-coinche.php) are the rules. The coinche is played between two teams of two players using a set of 32 classic cards (8 cards of each color - tile, clover, heart and spades). La Coinche is a strategic game similar to the Bridge. In Coinche, players must evaluate their hands and estimate the number of points they think they can reach in the game. Players make contracts and the ads have a major role in the game.

A round of Coinche could be divided into two distinct parts:
- First, given their hand, players propose a contrat (number of points to do + the suit)
- Secondly, the players play heigh tricks



## Objectif of the project

We want to apply Reinforcement Learning to Coinche. **To begin, we'll focus only on the second phase of a round. 
Players we'll be provided their eight cards' game and a contrat.**
The AI player will then have to both learn the rules and some strategies

One of the issue that we are facing would be the possibility to have the AI playing a card while it is not allow given 
the context. To prevent such position, we chose to deliver as output of the AI a vector of probability rather than a card. 
Therefore if the AI favors a card that can't be played, the gym envirronment will do a mask on the possible strokes and 
select the highest probability card favored by the AI


## Installation


We use the framework [gym](http://gym.openai.com/docs/) linked with [RL Coach](http://gym.openai.com/docs/) that provides deep learning algorithm.

Gym environment takes care of the game in itself (rules, rounds) and provide standard outputs to reiforcement learning algorithms based on steps
```
$ pip install requirements.txt
```

## Random score prediction and contrat selection

In order to simulate the contrat selection phase, we train a Machine Learning model on random games to predict the expected 
value of a game.
More precisly, given the player hands, we aimed at predicting the number of points the team won playing randomly against
a random team. Therefore we are able to predict if a game is "interesting" or not (regardless of the strategy)

The contrat selection phase is done as follow:
```
For each team:
    for each possible atout suit:
        compute the expected value of the game
    choose the best exepected value and the atout suit that comes with it

Select the attacking team that offers the best expected value and the atout suit that comes with it
```

 
To train the reward_model, run *_reward_prediction/train_reward_prediction_model.py_*.
It will generate a tf model, which weifhts are saved under h5 format.

Be sure to generate first the random data using [*_random_games_and_rewards_analysis.ipynb_*](https://github.com/EricPicot/gym-coinche/tree/master/reward_prediction).
 
*_NB: This approach could also be reused with policies different from random. It could even be more precise_*



## Training

To launch a training, you'll need a *_preset.py_* file and be sure to have correct registers in 
[__init__.py](https://github.com/EricPicot/gym-coinche/blob/master/coinche/gym/__init__.py).

A register should look like:
```
register(
    id='coinche-v1',
    entry_point='coinche.gym.env:GymCoinche',
    kwargs={
        'players': [
            AIPlayer("./path/to/checkpoint/chckp_name.ckpt", 0, "N"),
            RandomPlayer(1, "E"),
            GymPlayer(2, "S"),
            RandomPlayer(3, "W")
        ],
        'contrat_model_path': './reward_prediction/reward_model.h5'
    }
)
```
it contains:
- An id (mandatory ! It is the id that must be given in the preset.py)
- The entry point (do not change)
- kwargs
    - If you want to use specific policy agents (either pretrained policies or custom deterministic policies), file the 
    list. **BE CAREFULL, we  advise to keep the gymPlayer at index n°2**
    - If you want to use a model to predict the random score (see above) in order to simulate the contrat selection 
    phase, just give the path (Don't change the kwargs name)
    
Then, once you have change the levele name in the preset:
```
###############
# Environment #
###############
env_params = GymVectorEnvironment(level='coinche-v1') <--- change level name given the register
```
 you are ready to launch RL-coach using command line:
```
# to run a coach preset

$ coach -p ./preset.py -e coinche -ep ./experiments/ -s 270 -c

# To run a coach preset restarting training at a checkpoint
coach -p ./preset.py -e coinche -ep ./experiments/ -s 270 -c -crd ./path/to/checkpoint/

```

The training will be save in the directory ./experiments, and the tensorflow checkpoints will be saved every 270 seconds

You can then you the checkpoints policies will playing by calling :
 - ```AIPlayer("./path/to/checkpoint/chckp_name.ckpt", 0, "N")```


## Policy comparaison:

An important thing is to determine if a policy is better than another.
To do so, it is possible to make compete to policies against each other and to use statistical approach.

Please refer to *_policy_comparaison.ipynb_*:
It contains:
- the brick to simulates the game
- a quick description of the distribution of number o points won by each team
- a Statitistical test brick where H0 hypothesys is that there are no significant differencies between the two poilcies
## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[C.R.O.](https://fr.wikipedia.org/wiki/Coinche)

