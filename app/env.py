from .llm_agent import LLM_Agent
from .deck import Deck
from .player import Player

class CoincheEnv:
    def __init__(self):
        self.llm_agent = LLM_Agent('LLM_Agent')
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
        self.current_player_index = 0  # Track the current player in the annonce phase
        self.bidding_round = 0
        self.bidding_phase_over = False  # Flag to indicate if the bidding phase is over

    def initialize_game(self):
        self.current_contract = None
        self.current_contract_value = 70
        self.current_contract_holder = None
        self.atout_suit = None
        self.annonces = {player.name: None for player in self.players}  # Reset each player's latest annonce
        self.current_player_index = 0  # Reset the current player index
        self.bidding_round = 0
        self.bidding_phase_over = False  # Reset the bidding phase flag

        self.deck.reset()  # Reset the deck before dealing
        for player in self.players:
            player.reset_hand()  # Reset each player's hand
        hands = self.deck.deal(num_hands=4, num_cards_per_hand=8)
        for player, hand in zip(self.players, hands):
            player.receive_cards(hand)
            player.organize_hand()

    def handle_bidding(self, player_name, bid):
        if bid != 'pass':
            bid_value = int(bid.split()[0])
            if ((self.current_contract_value is None or bid_value > self.current_contract_value) 
                and (bid.split()[2] in ['hearts', 'spades', 'diamonds', 'clubs'])):
                self.current_contract_value = bid_value
                self.current_contract_holder = player_name
                self.current_contract = bid
                self.atout_suit = bid.split()[2]
                self.annonces[player_name] = bid
            else:  # the annonce is lower than current higher contract_value
                self.annonces[player_name] = 'pass'
        else:  # the annonce is lower than current higher contract_value
            self.annonces[player_name] = 'pass'
        print("Annonces: ", self.annonces)

        self.advance_bidding_round()
        return

    def advance_bidding_round(self):
        if self.bidding_phase_over:
            return  # End the recursion if the bidding phase is over

        self.current_player_index = (self.current_player_index + 1) % 4

        passes = [bid == 'pass' for bid in self.annonces.values()]
        reindexed_passes = passes[self.current_player_index:] + passes[:self.current_player_index]
        current_player = self.players[self.current_player_index]
        if all(reindexed_passes[-3:]) and all([bid is not None for bid in self.annonces.values()]):
            print("Three consecutive passes detected. Bidding phase ends.")
            self.bidding_phase_over = True  # Set the flag to indicate the bidding phase is over
            return  # End the bidding phase

        if not current_player.is_llm:
            self.render_bidding_options('South')
        else:
            annonce = self.llm_agent.get_annonce(current_player.name, 
                                                 current_player.hand, 
                                                 self.current_contract,
                                                 
                                                 self.current_contract_holder)
            self.handle_bidding(current_player.name, annonce)

    def render_bidding_options(self, player_name):
        options = self.get_bidding_options(player_name)
        self.send_bidding_options_to_frontend(player_name, options)

    def send_bidding_options_to_frontend(self, player_name, options):
        # This is a placeholder for sending options to the frontend
        print(f"Sending bidding options to {player_name}: {options}")

    def get_bidding_options(self, player_name):
        options = []
        if player_name == 'South':
            for suit in ['hearts', 'spades', 'diamonds', 'clubs']:
                for value in range(self.current_contract_value + 10, 170, 10):
                    options.append(f'{value} of {suit}')
        return {
            'options': options,
            'bidding_phase_over': self.bidding_phase_over
        }