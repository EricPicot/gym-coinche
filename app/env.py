from .llm_agent import LLM_Agent
from .deck import Deck
from .player import Player
import random

class CoincheEnv:
    def __init__(self, llm_api_key):
        self.llm_agent = LLM_Agent("LLM_Agent", llm_api_key)
        self.players = [Player(f"Player {i}") for i in range(4)]
        self.deck = Deck()

    def initialize_game(self):
        self.deck.reset()
        for player in self.players:
            player.reset_hand()  # Reset each player's hand
        hands = self.deck.deal(num_hands=4, num_cards_per_hand=8)
        for player, hand in zip(self.players, hands):
            player.receive_cards(hand)

    def annonce_phase(self, game_state):
        # Get annonce from LLM agent
        annonce = self.llm_agent.get_action(game_state)
        
        # Process the annonce (this is just an example)
        self.atout_suit = random.choice(["hearts", "diamonds", "clubs", "spades"])
        self.value = random.randint(80, 160)
        self.attacker_team = random.randint(0, 1)
        print(f"Annonce: {annonce}, Atout Suit: {self.atout_suit}, Value: {self.value}, Attacker Team: {self.attacker_team}")
        return {
            "annonce": annonce,
            "atout_suit": self.atout_suit,
            "value": self.value,
            "attacker_team": self.attacker_team
        }