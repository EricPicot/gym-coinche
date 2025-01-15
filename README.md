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

Ongoing !

## License
[C.R.O.](https://fr.wikipedia.org/wiki/Coinche)

