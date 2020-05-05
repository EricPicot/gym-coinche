import numpy as np
import random

from coinche.player import RandomPlayer
from coinche.gym.player import GymPlayer
from coinche.trick import Trick
from coinche.deck import Deck
from coinche.card import Suit
from coinche.utils import convert_cards_to_vector, convert_index_to_cards

from gym import Env, spaces


class GymCoinche(Env):
    def __init__(self):
        # observation_space
        # 32 played cards + 32 player cards + 32 cards of current trick + contract_value + attacker
        # 8 atouts + 8 suit 1 + 8 suit 2 + 8 suit 3
        # RL Coach observation_space has to be a Box
        self.observation_space = spaces.Box(low=0, high=1, shape=(98,))
        # 32 cards
        # 8 atouts + 8 suit 1 + 8 suit 2 + 8 suit 3
        self.action_space = spaces.Box(low=0, high=1, shape=(32,))

        self.players = [
            RandomPlayer(0, "N"), RandomPlayer(1, "E"), GymPlayer(2, "S"), RandomPlayer(3, "W")
        ]
        self.current_trick_rotation = []
        self.deck = Deck()
        self.round_number = 0
        self.played_tricks = []
        self.trick = None
        self.atout_suit = None
        self.value = None
        self.suits_order = None
        # TODO: select randomly the attacker_team in {0,1}
        self.attacker_team = 0

    def reset(self):
        """
        reset is mandatory to use gym framework. Reset is called at the end of each round (8 tricks)
        :return: observation
        """
        self._reset_round()
        self._play_until_end_of_rotation_or_ai_play()
        observation = self._get_trick_observation()
        return observation

    def step(self, action):
        """
        step is mandatory to use gym framework
        In each step, every player play exactly one, especially the AIPlayers.
        :param action:
        :return: observation, reward, done, info
        """
        self._play_gym(action)
        done = self._play_step()
        if not done:
            observation = self._get_trick_observation()
            current_player = self.current_trick_rotation[0]
            last_trick = self.played_tricks[-1]
            reward = self._get_trick_reward(last_trick, current_player)
            winning_team = 0 if last_trick.winner.index % 2 == 0 else 1
            info = {'winner': last_trick.winner.index,
                    'winning_team': winning_team}
            return observation, reward, done, info
        else:
            observation = self._get_round_observation()
            # TODO: define round reward
            reward = self._get_round_reward()
            info = {"player0-hand": self.player0_original_hand,
                    "player2-hand": self.player2_original_hand}
            return observation, reward, done, info

    def _reset_round(self):
        """
        Function called in the reset function. Called at each new round. Once all the important values are reset, and
        given the trick id (between 0 and 7) we define the first player of the first trick using np.roll.

        :return:
        """
        # New round
        self.round_number += 1

        # We rebuild the deck based on previous trick won by each players
        # TODO: Ordering previous played tricks by players
        self._rebuild_deck(self.played_tricks)
        self._deal_cards()
        self.played_tricks = []

        # Select color and value
        self.atout_suit = random.choice(list(Suit))  # select randomly the suit
        self.value = random.randint(0, 1)  # Can only announce 80 or 90 to begin with
        self.attacker_team = random.randint(0, 1)  # 0 if it is team 0 (player 0 and player 2) else 1 for team 1
        self.suits_order = Suit.create_order(self.atout_suit)

        # Set players attacker
        for p in self.players:
            p.attacker = int(self.attacker_team == p.index % 2)

        self.player0_original_hand = convert_cards_to_vector(self.players[0].cards, self.suits_order)
        self.player2_original_hand = convert_cards_to_vector(self.players[2].cards, self.suits_order)

        self.trick = Trick(self.atout_suit, trick_number=1)
        self.current_trick_rotation = self._create_trick_rotation(self.round_number % 4)

    def _rebuild_deck(self, played_tricks):
        # Check if duplicated cards
        for p in self.players:
            for trick in played_tricks:
                if p.index == trick.winner.index:
                    self.deck.add_trick(trick)
        self.deck.cut_deck()
        # TODO: remove this line
        self.deck = Deck()

    def _deal_cards(self):
        """
        This function deals the deck
        """
        players_round = np.roll(self.players, self.round_number)
        legal_dealing_sequences = [[3, 3, 2], [3, 2, 3]]  # Defining academic dealing sequences
        dealing_sequence = legal_dealing_sequences[random.randint(0, 1)]  # Choose the Dealing Sequence
        for cards_to_deal in dealing_sequence:
            for p in players_round:  # Stopping condition on one round
                p.add_cards(self.deck.deal(cards_to_deal))

    def _play_step(self):
        # Then play until end of trick
        self._play_until_end_of_rotation_or_ai_play()

        if len(self.current_trick_rotation) == 0:
            # Handle end of trick
            winner = self.trick.winner
            # add score to teams
            self.played_tricks.append(self.trick)

            # should stop if trick_number==8
            if len(self.played_tricks) == 8:
                return True

            self.trick = Trick(self.atout_suit, trick_number=len(self.played_tricks) + 1)
            # Choose next starter
            self.current_trick_rotation = self._create_trick_rotation(winner.index)
            # Play until AI
            self._play_until_end_of_rotation_or_ai_play()
            return False
        else:
            return False

    def _play_gym(self, action):
        current_player = self.current_trick_rotation[0]
        current_player.set_next_action(action)
        current_player.play_turn(self.trick, self.played_tricks, self.suits_order, self.value)
        self.current_trick_rotation.pop(0)

    def _play_until_end_of_rotation_or_ai_play(self):
        """
        When this method is called it is either:
        - An AIPlayer's turn: therefore we break and ask the AIPlayer to give prediction
        - Not an AIPlayer: therefore the current player just play given is deterministic (or random) policy

        :return:
        """
        while len(self.current_trick_rotation) > 0:
            current_player = self.current_trick_rotation[0]
            if isinstance(current_player, GymPlayer):
                break
            current_player.play_turn(self.trick, self.played_tricks, self.suits_order, self.value)
            self.current_trick_rotation.pop(0)

    def _get_trick_observation(self):
        # self.observation_space = [spaces.Discrete(2)] * (32 + 32 + 32) + [spaces.Discrete(10), spaces.Discrete(2)]
        played_cards = [card for trick in self.played_tricks for card in trick.cards]
        played_cards_observation = convert_cards_to_vector(played_cards, self.suits_order)
        current_player = self.current_trick_rotation[0]
        player_cards_observation = convert_cards_to_vector(current_player.cards, self.suits_order)
        trick_cards_observation = convert_cards_to_vector(self.trick.cards, self.suits_order)
        observation = np.concatenate((played_cards_observation,
                                      player_cards_observation,
                                      trick_cards_observation,
                                      [self.value / 9, current_player.attacker]))
        return observation

    def _get_round_observation(self):
        # self.observation_space = [spaces.Discrete(2)] * (32 + 32 + 32) + [spaces.Discrete(10), spaces.Discrete(2)]
        played_cards_observation = np.ones(32)
        player_cards_observation = np.zeros(32)
        trick_cards_observation = convert_cards_to_vector(self.trick.cards, self.suits_order)
        observation = np.concatenate((played_cards_observation,
                                      player_cards_observation,
                                      trick_cards_observation,
                                      [self.value / 9, 1]))
        return observation

    def _create_trick_rotation(self, starting_player_index):
        rotation = np.array(self.players)
        while rotation[0].index != starting_player_index:
            rotation = np.roll(rotation, 1)
        return rotation.tolist()

    def _get_trick_reward(self, trick, player):
        score = trick.score()
        score_factor = player.index % 2 == trick.winner.index % 2
        return score * score_factor

    def _get_round_reward(self):
        return 1
