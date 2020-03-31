from coinche.Player import AIPlayer, RandomPlayer
from coinche.Trick import Trick
from coinche.Deck import Deck
from coinche.exceptions import PlayException
from gym import Env, spaces
import numpy as np


class GymCoinche(Env):
    def __init__(self):
        self.observation_space = spaces.Box()
        self.action_space = spaces.Box()

        self.players = [
            RandomPlayer(0, "N"), RandomPlayer(1, "E"), AIPlayer(2, "S"), RandomPlayer(3, "W")
        ]
        self.current_trick_rotation = None
        self.deck = Deck()
        self.round_number = 0
        self.trick = None
        self.trick_number = 0
        self.color = None
        self.value = None
        # TODO: select randomly the attacker_team in {0,1}
        self.attacker_team = 0

        for p in self.players:
            if self.attacker_team == 0:
                if p.index % 2 == 0:
                    p.attacker = 1
                else:
                    p.attacker = 0
            elif self.attacker_team == 1:
                if p.index % 2 == 1:
                    p.attacker = 1
                else:
                    p.attacker = 0

    def reset(self):
        """
        reset is mandatory to use gym framework. Reset is called at the end of each round (8 tricks)
        :return: observation
        """
        self.play_reset()
        # TODO: create observation
        observation = []
        return observation

    def step(self, action):
        """
        step is mandatory to use gym framework
        In each step, every player play exactly one, especially the AIPlayers.
        :param action:
        :return: observation, reward, done, info
        """
        # TODO: play for ai
        self.play_step()
        # TODO: create observation
        observation = []
        return observation, reward, done, info

    def play_reset(self):
        """
        Function called in the reset function. Called at each new round. Once all the important values are reset, and
        given the trick id (between 0 and 7) we define the first player of the first trick using np.roll.

        :return:
        """
        # Select color and value
        self.color = None
        self.value = None
        self.trick_number = 0
        self.round_number += 1
        self.attacker_team = 0  # 0 if it is team 0 (player 0 and player 2) else 1 for team 1

        for p in self.players:
            if self.attacker_team == 0:
                if p.index % 2 == 0:
                    p.attacker = 1
                else:
                    p.attacker = 0
            elif self.attacker_team == 1:
                if p.index % 2 == 1:
                    p.attacker = 1
                else:
                    p.attacker = 0

        self.deck.shuffle()
        # TODO: deal for players in Deck
        # [ [card, card, card, card], [], [], [] ]
        cards = self.deck.deal()
        players_round = np.roll(self.players, self.round_number)
        for p, c in zip(players_round, cards):
            p.addCards(c)

        self.trick = Trick(self.color, self.trick_number)
        self.current_trick_rotation = self._create_trick_rotation(self.round_number % 4)
        self._play_until_end_of_rotation_or_ai_play()

    def play_step(self):
        # Play until end of trick
        self._play_until_end_of_rotation_or_ai_play()

        # Handle end of trick
        # TODO: can be removed
        assert self.trick.is_done()
        winner = self.trick.winner
        score = self.trick.score()
        trick_cards = self.trick.trick
        # add score to teams
        self.trick_number += 1
        self.trick = Trick(self.color, self.trick_number)
        # Choose next starter
        self.current_trick_rotation = self._create_trick_rotation(winner)
        # Play until AI
        self._play_until_end_of_rotation_or_ai_play()

    def _create_trick_rotation(self, starting_player_index):
        rotation = self.players
        while rotation[0].index != starting_player_index:
            rotation = np.roll(rotation, 1)
        return rotation

    def _play_until_end_of_rotation_or_ai_play(self):
        """
        When this method is called it is either:
        - An AIPlayer's turn: therefore we break and ask the AIPlayer to give prediction
        - Not an AIPlayer: therefore the current player just play given is deterministic (or random) policy

        :return:
        """
        while len(self.current_trick_rotation) > 0:
            p = self.current_trick_rotation.pop()
            if isinstance(p, AIPlayer):
                break

            # Ask not ai player to player (could be random)
            if not isinstance(p, AIPlayer):
                while True:
                    # TODO: dev a deterministic player
                    card = p.getRandom()
                    try:
                        self.trick.addCard(card, p.hand, p.index)
                        break
                    except PlayException:
                        pass
