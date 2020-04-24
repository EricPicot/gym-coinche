import numpy as np
import tensorflow as tf
from random import choice
from coinche.exceptions import PlayException


class Player:
    def __init__(self, index, name):
        self.index = index
        self.name = name
        self.cards = []
        self.score = 0
        self.team = None
        self.teammate = None
        self.attacker = None

    def add_cards(self, cards):
        self.cards += cards

    def has_card(self, card):
        return card in self.cards

    def has_suit(self, suit):
        for card in self.cards:
            if card.suit == suit:
                return True
        return False

    def get_suit_card(self, suit):
        suit_cards = []

        for card in self.cards:
            if card.suit == suit:
                suit_cards.append(card)
        return suit_cards

    def remove_card(self, card):
        self.cards.remove(card)

    def reset_round(self):
        self.score = 0

    def play_turn(self, trick):
        while True:
            try:
                card = self.get_turn_card(trick)
                trick.add_card(card, self)
                self.remove_card(card)
                break
            except PlayException as e:
                continue

    def get_turn_card(self, trick):
        raise NotImplementedError()


class RandomPlayer(Player):
    def get_turn_card(self, _trick):
        return choice(self.cards)


class DeterministicPlayer(RandomPlayer):
    def get_turn_card(self, trick):
        # If player is the first to start
        if trick.cardsInTrick == 0:
            # If player is an attacker
            if self.attacker == 1:
                # Try to play Atout or play random card
                if self.has_suit(trick.atout_suit):
                    suit_cards = self.get_suit_card(trick.atout_suit)
                    return choice(suit_cards)
                else:
                    return choice(self.cards)
        return choice(self.cards)


class GymPlayer(Player):
    def get_turn_card(self, _trick):
        raise NotImplementedError()


class AIPlayer(Player):
    def __init__(self, index, name, checkpoint_path):
        super(AIPlayer, self).__init__(index, name)
        self.input_tensor = "main_level/agent/policy/online/network_0/observation/observation:0"
        self.output_tensor = "main_level/agent/policy/online/network_0/sac_policy_head_0/policy_mean:0"

        self.sess = tf.compat.v1.Session()
        saver = tf.compat.v1.train.import_meta_graph(checkpoint_path + ".meta")
        saver.restore(self.sess, checkpoint_path)

    def get_turn_card(self, trick):
        # TODO: create observation
        trick_observation = np.random.uniform(0, 1, 98)
        trick_observation = np.expand_dims(trick_observation, axis=0)
        actions = self.sess.run(self.output_tensor, {self.input_tensor: trick_observation})
        action = np.squeeze(actions, axis=0)

        # TODO: create observation
        player_cards_observation = self._create_cards_observation(self.cards)
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
                break
            except PlayException:
                continue


