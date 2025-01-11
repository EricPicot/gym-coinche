from flask import Blueprint, request, jsonify
from .env import CoincheEnv

main = Blueprint('main', __name__)
env = CoincheEnv(llm_api_key="your_openai_api_key")

@main.route('/initialize', methods=['POST'])
def initialize():
    env.initialize_game()
    players_hands = {player.name: [str(card) for card in player.hand] for player in env.players}
    return jsonify(players_hands)

@main.route('/annonce', methods=['POST'])
def annonce():
    game_state = request.json.get('game_state')
    annonce = env.annonce_phase(game_state)
    return jsonify({"annonce": annonce})