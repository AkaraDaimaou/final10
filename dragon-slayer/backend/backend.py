from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

# File to store game state
STATE_FILE = 'game_state.json'

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return {"difficulty": "EASY", "game_state": "MENU"}

def save_state(state):
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f)

@app.route('/start', methods=['POST'])
def start_game():
    difficulty = request.json.get('difficulty', 'EASY')
    state = load_state()
    state['difficulty'] = difficulty
    state['game_state'] = 'PLAYING'
    save_state(state)
    return jsonify({"status": "Game started", "difficulty": difficulty})

@app.route('/difficulty', methods=['POST'])
def set_difficulty():
    difficulty = request.json.get('difficulty', 'EASY')
    state = load_state()
    state['difficulty'] = difficulty
    save_state(state)
    return jsonify({"status": "Difficulty set", "difficulty": difficulty})

if __name__ == '__main__':
    app.run(debug=True)
