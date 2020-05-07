import numpy as np
import tensorflow as tf
from random import choice, sample
from coinche.utils import convert_cards_to_vector, convert_index_to_cards
from coinche.exceptions import PlayException


class Player:
    def __init__(self, index, name):
        self.index = index
        self.name = name
        self.cards = []
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

    def play_turn(self, trick, played_tricks, suits_order, contract_value):
        cards_order = self.get_cards_order(trick, played_tricks, suits_order, contract_value)
        for card in cards_order:
            try:
                trick.add_card(card, self)
                self.remove_card(card)
                break
            except PlayException as e:
                continue

    def get_cards_order(self, trick, played_tricks, suits_order, contract_value):
        raise NotImplementedError()


class RandomPlayer(Player):
    def get_cards_order(self, _trick, _played_tricks, _suits_order, _contract_value):
        return sample(self.cards, len(self.cards))


class DeterministicPlayer(RandomPlayer):
    def get_cards_order(self, trick, _played_tricks, _suits_order, _contract_value):
        return self.cards


class AIPlayer(Player):
    def __init__(self, checkpoint_path, *args, **kwargs):
        super(AIPlayer, self).__init__(*args, **kwargs)
        self.input_tensor = "main_level/agent/policy/online/network_0/observation/observation:0"
        self.output_tensor = "main_level/agent/policy/online/network_0/sac_policy_head_0/policy_mean:0"
        self.graph = tf.Graph()
        self.sess = tf.compat.v1.Session(graph=self.graph)
        with self.sess.as_default():
            with self.graph.as_default():
                tf.global_variables_initializer().run()
                saver = tf.compat.v1.train.import_meta_graph(checkpoint_path + ".meta")
                saver.restore(self.sess, checkpoint_path)

    def get_cards_order(self, trick, played_tricks, suits_order, contract_value):
        # Create observation
        played_cards = [card for trick in played_tricks for card in trick.cards]
        played_cards_observation = convert_cards_to_vector(played_cards, suits_order)
        player_cards_observation = convert_cards_to_vector(self.cards, suits_order)
        trick_cards_observation = convert_cards_to_vector(trick.cards, suits_order)
        trick_observation = np.concatenate((played_cards_observation,
                                            player_cards_observation,
                                            trick_cards_observation,
                                            [contract_value / 9, self.attacker]))
        trick_observation = np.expand_dims(trick_observation, axis=0)
        with self.sess.as_default():
            with self.graph.as_default():
                actions = self.sess.run(self.output_tensor, {self.input_tensor: trick_observation})
        action = np.squeeze(actions, axis=0)

        player_cards_observation = convert_cards_to_vector(self.cards, suits_order)
        player_action_masked = player_cards_observation * action

        # Play cards in probability order
        if np.max(player_action_masked) > 0:
            cards_index_order = np.argsort(-player_action_masked)
        else:
            cards_index_order = np.argsort(-player_cards_observation)
        return convert_index_to_cards(cards_index_order, suits_order)
