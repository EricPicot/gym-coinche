from flask import Blueprint, request, jsonify
from flask_cors import CORS
from .env import CoincheEnv

main = Blueprint('main', __name__)
CORS(main)  # Enable CORS for the blueprint
env = CoincheEnv()

@main.route('/initialize', methods=['POST'])
def initialize():
    env.initialize_game()
    players_hands = {player.name: [str(card) for card in player.hand] for player in env.players}
    for player in env.players:
        print(f"{player.name}: {player.hand}")
        # Fetch initial bidding options for the human player (South)
    bidding_options = env.get_bidding_options('South')
    print("Bidding options Initialization: ", bidding_options)
    return jsonify({
        'players_hands': players_hands,
        'bidding_options': bidding_options['options'],
        'bidding_phase_over': bidding_options['bidding_phase_over'],
        'annonces': env.annonces  # Include annonces in the response
    })

@main.route('/game_state', methods=['GET'])
def game_state():
    return jsonify(env.get_game_state())

@main.route('/bid', methods=['POST'])
def bid():
    data = request.json
    player = data['player']
    bid = data['bid']
    print("Player", player)
    print("Bid", bid)
    env.handle_bidding(player, bid)
    return jsonify({'status': 'success'})

@main.route('/get_bidding_options', methods=['GET'])
def get_bidding_options():
    print("Getting bidding options")
    player = request.args.get('player')
    print("Player", player)
    options = env.get_bidding_options(player)
    print("options: ", options)
    return jsonify({
        'options': options['options'],
        'bidding_phase_over': options['bidding_phase_over'],
        'annonces': env.annonces  # Include annonces in the response
    })