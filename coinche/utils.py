import numpy as np
from coinche.card import Card


def convert_cards_to_vector(cards, suits_order):
    cards_vector = np.zeros(32)

    for card in cards:
        card_position = card.to_index(suits_order)
        np.put(cards_vector, card_position, 1)
    return cards_vector


def convert_index_to_cards(cards_index, suits_order):
    return [Card.from_index(card_index, suits_order) for card_index in cards_index]
