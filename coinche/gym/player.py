import numpy as np

from coinche.player import Player
from coinche.utils import convert_cards_to_vector, convert_index_to_cards


class GymPlayer(Player):
    def __init__(self, *args, **kwargs):
        super(GymPlayer, self).__init__(*args, **kwargs)
        self.next_action = None

    def set_next_action(self, action):
        self.next_action = action

    def get_cards_order(self, _trick, _played_tricks, suits_order, _contract_value):
        if self.next_action is None:
            raise RuntimeError("Action should be filled.")
        player_cards_observation = convert_cards_to_vector(self.cards, suits_order)
        player_action_masked = player_cards_observation * self.next_action

        # Play cards in probability order
        if np.max(player_action_masked) > 0:
            cards_index = np.argsort(-player_action_masked)
        else:
            cards_index = np.argsort(-player_cards_observation)
        cards_play_order = convert_index_to_cards(cards_index, suits_order)
        self.next_action = None
        return cards_play_order
