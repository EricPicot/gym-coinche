import numpy as np
import random

from coinche.player import RandomPlayer, AIPlayer
from coinche.gym.player import GymPlayer
from coinche.trick import Trick
from coinche.deck import Deck
from coinche.card import Suit
from coinche.utils import convert_cards_to_vector
from coinche.reward_prediction import decision_process

from gym import Env, spaces
from tensorflow.keras import models


class GymCoinche(Env):
    def __init__(self, players=None, contrat_model_path=None):
        # observation_space
        # 32 played cards + 32 player cards + 32 cards of current trick + contract_value + attacker
        # 8 atouts + 8 suit 1 + 8 suit 2 + 8 suit 3
        # RL Coach observation_space has to be a Box
        self.observation_space = spaces.Box(low=0, high=1, shape=(98,))
        # 32 cards
        # 8 atouts + 8 suit 1 + 8 suit 2 + 8 suit 3
        self.action_space = spaces.Box(low=0, high=1, shape=(32,))

        self.players = players if players is not None else [
            RandomPlayer(0, "N"),
            RandomPlayer(1, "E"),
            GymPlayer(2, "S"),
            RandomPlayer(3, "W")
        ]
        self.current_trick_rotation = []
        self.deck = Deck()
        self.round_number = 0
        self.played_tricks = []
        self.trick = None
        self.atout_suit = None
        self.value = None
        self.suits_order = None
        self.contrat_model = models.load_model(contrat_model_path) if contrat_model_path is not None else None
        print("Contrat model passed: ", contrat_model_path)
        self.attacker_team = 0
        self.original_hands = {}

    def reset(self):
        """
        reset is mandatory to use gym framework. Reset is called at the end of each round (8 tricks)
        :return: observation
        """
        # New round
        self.round_number += 1

        # We rebuild the deck based on previous trick won by each players
        self._rebuild_deck(self.played_tricks)
        self._deal_cards()
        self.played_tricks = []

        # Get value of the contract and attacker team and updates suits order
        if self.contrat_model is None:
            self.atout_suit = random.choice(list(Suit))  # select randomly the suit
            self.value = random.randint(0, 1)  # Can only announce 80 or 90 to begin with
            self.attacker_team = random.randint(0, 1)  # 0 if it is team 0 (player 0 and player 2) else 1 for team 1
            self.suits_order = Suit.create_order(self.atout_suit)
        else:
            self._set_contrat(self.contrat_model)

        # Set players attacker
        for p in self.players:
            p.attacker = int(self.attacker_team == p.index % 2)

        self.original_hands = {
            "player0-hand": convert_cards_to_vector(self.players[0].cards, self.suits_order),
            "player1-hand": convert_cards_to_vector(self.players[1].cards, self.suits_order),
            "player2-hand": convert_cards_to_vector(self.players[2].cards, self.suits_order),
            "player3-hand": convert_cards_to_vector(self.players[3].cards, self.suits_order),
            "attacker_team": [p.attacker for p in self.players]
        }
        self.total_score = 0
        self.trick = Trick(self.atout_suit, trick_number=1)
        self.current_trick_rotation = self._create_trick_rotation(self.round_number % 4)

        # Play until AI
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
        # Play for gym player
        ai_player = self.current_trick_rotation[0]
        ai_player.set_next_action(action)
        ai_player.play_turn(self.trick, self.played_tricks, self.suits_order, self.value)
        self.current_trick_rotation.pop(0)
        # Then play until end of trick
        self._play_until_end_of_rotation_or_ai_play()
        # Handle end of trick
        winner = self.trick.winner
        trick_score_factor = ai_player.index % 2 == winner.index % 2
        reward = self._get_reward(self.trick,
                                  self.total_score,
                                  trick_score_factor,
                                  self.value)
        # add score to teams
        self.played_tricks.append(self.trick)

        # Add trick score to total_score
        self.total_score += self._get_trick_reward(self.trick, trick_score_factor)

        if len(self.played_tricks) < 8:
            self.trick = Trick(self.atout_suit, trick_number=len(self.played_tricks) + 1)
            # Choose next starter
            self.current_trick_rotation = self._create_trick_rotation(winner.index)
            # Play until AI
            self._play_until_end_of_rotation_or_ai_play()
            observation = self._get_trick_observation()
            winning_team = 0 if winner.index % 2 == 0 else 1
            info = {'winner': winner.index,
                    'winning_team': winning_team}
            return observation, reward, False, info
        else:
            observation = self._get_round_observation()
            info = self.original_hands
            info["total_reward"] = self.total_score
            return observation, reward, True, info

    def _set_contrat(self, contrat_model):
        default_suit_order = list(Suit)

        hand0 = convert_cards_to_vector(self.players[0].cards, default_suit_order)
        hand1 = convert_cards_to_vector(self.players[1].cards, default_suit_order)
        hand2 = convert_cards_to_vector(self.players[2].cards, default_suit_order)
        hand3 = convert_cards_to_vector(self.players[3].cards, default_suit_order)

        shift_team1, expected_reward_team1 = decision_process(hand0, hand2, contrat_model)
        shift_team2, expected_reward_team2 = decision_process(hand1, hand3, contrat_model)

        if expected_reward_team1 > expected_reward_team2:
            expected_reward_team = expected_reward_team1
            attacker_team = 0
            shift = shift_team1
        else:
            expected_reward_team = expected_reward_team2
            attacker_team = 1
            shift = shift_team2

        # Carefull: shifting is anti-clockwise
        self.atout_suit = default_suit_order[-shift]
        self.suits_order = Suit.create_order(self.atout_suit)

        self.value = np.max([0, (expected_reward_team//10) - 8])/9
        self.attacker_team = attacker_team

    def _rebuild_deck(self, played_tricks):
        # Check if duplicated cards
        for p in self.players:
            for trick in played_tricks:
                if p.index == trick.winner.index:
                    self.deck.add_trick(trick)
        self.deck.cut_deck()

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
                                      [self.value, current_player.attacker]))
        return observation

    def _get_round_observation(self):
        # self.observation_space = [spaces.Discrete(2)] * (32 + 32 + 32) + [spaces.Discrete(10), spaces.Discrete(2)]
        played_cards_observation = np.ones(32)
        player_cards_observation = np.zeros(32)
        trick_cards_observation = convert_cards_to_vector(self.trick.cards, self.suits_order)
        observation = np.concatenate((played_cards_observation,
                                      player_cards_observation,
                                      trick_cards_observation,
                                      [self.value, 1]))
        return observation

    def _create_trick_rotation(self, starting_player_index):
        rotation = np.array(self.players)
        while rotation[0].index != starting_player_index:
            rotation = np.roll(rotation, 1)
        return rotation.tolist()

    def _get_trick_reward(self, trick, trick_score_factor):
        score = trick.score()
        return score * trick_score_factor

    def _get_reward(self, trick, total_score, trick_score_factor, value, normalisation_trick=10):
        # trick reward: if not last trick
        if True:
            score = trick.score()
            if trick_score_factor:
                return score  / normalisation_trick
            else:
                return - score / normalisation_trick
        # if True:
        #     score = trick.score()
        #     if trick_score_factor:
        #         return np.exp(score  / normalisation_trick)
        #     else:
        #         return - np.exp(score / normalisation_trick)

        # if this is last trick of round
#         else:
# #          Let's check if contract is done
#             if ((total_score/10) - 8)/9 >= value:
#                 return 9
#             else:
#                 return -9

