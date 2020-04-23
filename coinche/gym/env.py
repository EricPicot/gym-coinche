from coinche.player import AIPlayer, RandomPlayer
from coinche.trick import Trick
from coinche.deck import Deck
from coinche.card import Card, Rank, Suit
from coinche.exceptions import PlayException
from gym import Env, spaces
import numpy as np
import random


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
            RandomPlayer(0, "N"), RandomPlayer(1, "E"), AIPlayer(2, "S"), RandomPlayer(3, "W")
        ]
        self.current_trick_rotation = []
        self.deck = Deck()
        self.round_number = 0
        self.played_tricks = []
        self.trick = None
        self.atout_suit = None
        self.value = None
        # TODO: select randomly the attacker_team in {0,1}
        self.attacker_team = 0

        self.suits_order = [suit for suit in Suit]

    def reset(self):
        """
        reset is mandatory to use gym framework. Reset is called at the end of each round (8 tricks)
        :return: observation
        """
        self._play_reset()
        observation = self._get_trick_observation()
        return observation

    def step(self, action):
        """
        step is mandatory to use gym framework
        In each step, every player play exactly one, especially the AIPlayers.
        :param action:
        :return: observation, reward, done, info
        """
        done = self._play_step(action)
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

    def _get_trick_reward(self, trick, player):
        score = trick.score()
        score_factor = player.index % 2 == trick.winner.index % 2
        return score * score_factor

    def _get_round_reward(self):
        return 1

    def _play_reset(self):
        """
        Function called in the reset function. Called at each new round. Once all the important values are reset, and
        given the trick id (between 0 and 7) we define the first player of the first trick using np.roll.

        :return:
        """
        # Select color and value
        self.round_number += 1

        self.atout_suit = random.choice(self.suits_order)  # select randomly the suit
        self.value = random.randint(0, 1)  # Can only announce 80 or 90 to begin with
        self.attacker_team = random.randint(0, 1)  # 0 if it is team 0 (player 0 and player 2) else 1 for team 1
        self.suits_order = self._define_suits_order(self.suits_order)

        # We rebuild the deck based on previous trick won by each players
        # TODO: Ordering previous played tricks by players
        self._rebuild_deck(self.played_tricks)
        self.played_tricks = []

        # Set players attacker
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
        #  -----
        for p in self.players:
            p.reset_round()

        # -----
        self._deal_cards()

        self.player0_original_hand = self._create_cards_observation(self.players[0].cards)
        self.player2_original_hand = self._create_cards_observation(self.players[2].cards)

        self.trick = Trick(self.atout_suit, trick_number=1)
        self.current_trick_rotation = self._create_trick_rotation(self.round_number % 4)
        self._play_until_end_of_rotation_or_ai_play()

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
        legalDealingSequences = [[3, 3, 2], [3, 2, 3]]  # Defining academic dealing sequences
        dealingSequence = legalDealingSequences[random.randint(0, 1)]  # Choose the Dealing Sequence
        for cardsToDeal in dealingSequence:
            for p in players_round:  # Stopping condition on one round
                p.add_cards(self.deck.deal(cardsToDeal))


    def _play_step(self, action):
        # AI has to play
        self._play_ai(action)
        # Then play until end of trick
        self._play_until_end_of_rotation_or_ai_play()

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

    def _play_ai(self, action):
        current_player = self.current_trick_rotation[0]
        player_cards_observation = self._create_cards_observation(current_player.cards)
        player_action_masked = player_cards_observation * action

        # Play cards in probability order
        if np.max(player_action_masked) > 0:
            cards_index = np.argsort(-player_action_masked)
        else:
            cards_index = np.argsort(-player_cards_observation)
        for card_index in cards_index:
            try:
                card_rank = (card_index % 8)
                card_suit = int(card_index / 8)
                card = Card(Rank(card_rank), Suit(self.suits_order[card_suit]))
                self.trick.add_card(card, current_player)
                current_player.remove_card(card)
                self.current_trick_rotation.pop(0)
                break
            except PlayException:
                continue

    def _create_trick_rotation(self, starting_player_index):
        rotation = np.array(self.players)
        while rotation[0].index != starting_player_index:
            rotation = np.roll(rotation, 1)
        return rotation.tolist()

    def _get_trick_observation(self):
        # self.observation_space = [spaces.Discrete(2)] * (32 + 32 + 32) + [spaces.Discrete(10), spaces.Discrete(2)]
        played_cards = [card for trick in self.played_tricks for card in trick.cards]
        played_cards_observation = self._create_cards_observation(played_cards)
        current_player = self.current_trick_rotation[0]
        player_cards_observation = self._create_cards_observation(current_player.cards)
        trick_cards_observation = self._create_cards_observation(self.trick.cards)
        attacker = current_player.attacker
        contract_value = self.value / 9
        observation = np.concatenate((played_cards_observation,
                                      player_cards_observation,
                                      trick_cards_observation,
                                      [contract_value, attacker]))
        return observation

    def _get_round_observation(self):
        # self.observation_space = [spaces.Discrete(2)] * (32 + 32 + 32) + [spaces.Discrete(10), spaces.Discrete(2)]
        played_cards_observation = np.ones(32)
        player_cards_observation = np.zeros(32)
        trick_cards_observation = self._create_cards_observation(self.trick.cards)
        # TODO: to do
        attacker = 1
        contract_value = self.value / 9
        observation = np.concatenate((played_cards_observation,
                                      player_cards_observation,
                                      trick_cards_observation,
                                      [contract_value, attacker]))
        return observation

    def _create_cards_observation(self, cards):
        cards_observation = np.zeros(32)

        for card in cards:
            if card.suit == -1:
                continue
            suit_position = self.suits_order.index(card.suit)
            rank_position = card.rank.value
            card_position = rank_position + (suit_position * 8)
            np.put(cards_observation, card_position, 1)
        return cards_observation

    def _play_until_end_of_rotation_or_ai_play(self):
        """
        When this method is called it is either:
        - An AIPlayer's turn: therefore we break and ask the AIPlayer to give prediction
        - Not an AIPlayer: therefore the current player just play given is deterministic (or random) policy

        :return:
        """
        while len(self.current_trick_rotation) > 0:
            current_player = self.current_trick_rotation[0]
            if isinstance(current_player, AIPlayer):
                break

            # Ask not ai player to player (could be random)
            if not isinstance(current_player, AIPlayer):
                while True:
                    # TODO: dev a deterministic player
                    try:
                        # TODO: play_turn
                        card = current_player.get_random()
                        self.trick.add_card(card, current_player)
                        current_player.remove_card(card)
                        self.current_trick_rotation.pop(0)
                        break
                    except PlayException as e:
                        continue

    def _define_suits_order(self, suits_order):
        tmp_suits_order = np.array(suits_order)
        while True:
            if tmp_suits_order[0] == self.atout_suit:
                break
            tmp_suits_order = np.roll(tmp_suits_order, 1)
        return tmp_suits_order.tolist()
