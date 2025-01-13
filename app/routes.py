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
    return jsonify(players_hands)

@main.route('/annonce', methods=['POST', 'OPTIONS'])
def annonce():
    if request.method == 'OPTIONS':
        print("OPTIONS request received")
        return jsonify({'status': 'ok'}), 200

    print("POST request received")
    data = request.json
    print("Data", data)
    if data.get('human_annonce') == 'pass':
        annonce_result = env.annonce_phase({"value": 0, "suit": "pass"})
    else:
        annonce_result = env.annonce_phase(data.get('human_annonce'))
    return jsonify({"annonce": annonce_result})