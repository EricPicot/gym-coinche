from .llm_agent import LLM_Agent
from .deck import Deck
from .player import Player

class CoincheEnv:
    def __init__(self):
        self.llm_agent = LLM_Agent("LLM_Agent")
        self.players = [
            Player("South", is_llm=False),  # Human player
            Player("West", is_llm=True),
            Player("North", is_llm=True),
            Player("East", is_llm=True)
        ]
        self.deck = Deck()
        self.current_contract = None
        self.current_contract_value = 70
        self.current_contract_holder = None
        self.atout_suit = None
        self.annonces = {player.name: None for player in self.players}  # Track each player's latest annonce

    def initialize_game(self):
        self.current_contract = None
        self.current_contract_value = 70
        self.current_contract_holder = None
        self.atout_suit = None
        self.annonces = {player.name: None for player in self.players}  # Reset each player's latest annonce

        self.deck.reset()  # Reset the deck before dealing
        for player in self.players:
            player.reset_hand()  # Reset each player's hand
        hands = self.deck.deal(num_hands=4, num_cards_per_hand=8)
        for player, hand in zip(self.players, hands):
            player.receive_cards(hand)
            player.organize_hand()

            
    def annonce_phase(self, human_annonce):
        passes = 0
        while passes < 3:
            for player in self.players:
                if self.current_contract_holder == player.name:
                    break
                elif player.is_llm:
                    annonce = self.llm_agent.get_annonce(player.name, player.hand, self.current_contract, self.current_contract_holder)
                else:
                    print('human_annonce: ', human_annonce)
                    if human_annonce['suit'] == "pass":
                        annonce = "pass"
                    else:
                        annonce = f"{human_annonce['value']} of {human_annonce['suit']}"

                if annonce == "pass":
                    passes += 1
                else:
                    value, suit = [x.strip() for x in annonce.split('of')]
                    value = int(value)
                    if value > self.current_contract_value:
                        self.current_contract = annonce
                        self.current_contract_value = value
                        self.current_contract_holder = player.name
                        self.atout_suit = suit
                        self.annonces[player.name] = annonce
                        passes = 0  # Reset passes if a higher annonce is made
                    else:
                        passes += 1

        print("Annonce phase completed")
        print(f"Final contract value: {self.current_contract_value}")
        print(f"Contract holder: {self.current_contract_holder}")
        print(f"Atout suit: {self.atout_suit}")

        return {
            "current_contract_value": self.current_contract_value,
            "current_contract_holder": self.current_contract_holder,
            "atout_suit": self.atout_suit,
            "annonces": self.annonces  # Return the latest annonces
        }