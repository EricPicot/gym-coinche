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

One of the issue that we are facing would be the possibility to have the AI playing a card while it is not allow given the context. To prevent such position, we chose to deliver as output of the AI a vector of probability rather than a card. Therefore if the AI favors a card that can't be played, the gym envirronment will do a mask on the possible strokes and select the highest probability card favored by the AI

## Score prediction

To train the reward_model, run reward_predict.py.
It will generate a tf model, which weifhts are saved under h5 format


## Installation


We use the framework [gym](http://gym.openai.com/docs/) linked with [RL Coach](http://gym.openai.com/docs/) that provides deep learning algorithm.

Gym environment takes care of the game in itself (rules, rounds) and provide standard outputs to reiforcement learning algorithms based on steps
```
$ pip install requirements.txt

# to run a coach preset

$ coach -p ./preset.py -e coinche -ep ./experiments/
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[C.R.O.](https://fr.wikipedia.org/wiki/Coinche)

