# main.py
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from supabase import create_client, Client
import threading
import time  

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app)

# Initialize Supabase client
supabase_url = "https://bmzebewzxpnheeuhuplh.supabase.co"
supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJtemViZXd6eHBuaGVldWh1cGxoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjExNzg0MzQsImV4cCI6MjAzNjc1NDQzNH0.sWY8GLXn2-8MMzNpYYShXejONE9qYWhRuW0IivQX2GM"

supabase: Client = create_client(supabase_url, supabase_key)

waiting_players = []

def match_players():
    while True:
        if len(waiting_players) >= 2:
            player1 = waiting_players.pop(0)
            player2 = waiting_players.pop(0)
            socketio.emit('match_found', {'player1': player1, 'player2': player2}, room=player1)
            socketio.emit('match_found', {'player1': player1, 'player2': player2}, room=player2)
        time.sleep(1)

@socketio.on('register')
def handle_register(data):
    waiting_players.append(request.sid)
    socketio.send(request.sid, 'waiting_for_opponent')

@app.route('/register', methods=['POST'])
def register():
    email = request.json.get('email')
    password = request.json.get('password')
    try:
        user = supabase.auth.sign_up(email, password)
        return jsonify({'status': 'success', 'user': user}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@app.route('/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')
    try:
        user = supabase.auth.sign_in(email, password)
        return jsonify({'status': 'success', 'user': user}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@app.route('/start', methods=['POST'])
def start_game():
    difficulty = request.json.get('difficulty', 'easy')  # Default to 'easy'
    flappy_dragon_game.difficulty = difficulty
    flappy_dragon_game.reset_game()
    flappy_dragon_game.main()
    return jsonify({"status": "Game started", "difficulty": difficulty})

@app.route('/difficulty', methods=['POST'])
def set_difficulty():
    difficulty = request.json.get('difficulty', 'easy')  # Default to 'easy'
    flappy_dragon_game.difficulty = difficulty
    flappy_dragon_game.reset_game()
    return jsonify({"status": "Difficulty set", "difficulty": difficulty})

@app.route('/save-progress', methods=['POST'])
def save_progress():
    data = request.json
    user_id = data.get('user_id')
    level = data.get('level')
    score = data.get('score')
    
    if user_id and level is not None and score is not None:
        response = supabase.table('game_progress').insert({
            'user_id': user_id,
            'level': level,
            'score': score
        }).execute()
        if response.status_code == 201:
            return jsonify({'status': 'success', 'data': response.data}), 201
        else:
            return jsonify({'status': 'error', 'message': 'Failed to save progress'}), 500
    else:
        return jsonify({'status': 'error', 'message': 'Invalid data'}), 400

@app.route('/save-highscore', methods=['POST'])
def save_highscore():
    data = request.json
    user_id = data.get('user_id')
    score = data.get('score')
    
    if user_id and score is not None:
        response = supabase.table('high_scores').insert({
            'user_id': user_id,
            'score': score
        }).execute()
        if response.status_code == 201:
            return jsonify({'status': 'success', 'data': response.data}), 201
        else:
            return jsonify({'status': 'error', 'message': 'Failed to save high score'}), 500
    else:
        return jsonify({'status': 'error', 'message': 'Invalid data'}), 400

if __name__ == '__main__':
    threading.Thread(target=match_players).start()
    socketio.run(app, debug=True)
