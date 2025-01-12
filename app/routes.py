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
    data = request.json
    player_index = data.get('player_index')
    current_contract_value = data.get('current_contract_value')
    current_contract_holder = data.get('current_contract_holder')
    annonce_result = env.annonce_phase(player_index, current_contract_value, current_contract_holder)
    return jsonify({"annonce": annonce_result})