from flask import Flask, jsonify, request
from flask_cors import CORS
import pygame
import os
import sys
import random

import supabase

app = Flask(__name__)
CORS(app)

# Existing code...
# Initialize Supabase client

NEXT_PUBLIC_SUPABASE_URL = "https://bmzebewzxpnheeuhuplh.supabase.co"
NEXT_PUBLIC_SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJtemViZXd6eHBuaGVldWh1cGxoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjExNzg0MzQsImV4cCI6MjAzNjc1NDQzNH0.sWY8GLXn2-8MMzNpYYShXejONE9qYWhRuW0IivQX2GM"
supabase_client = supabase.create_client(NEXT_PUBLIC_SUPABASE_URL, NEXT_PUBLIC_SUPABASE_ANON_KEY)

@app.route('/register', methods=['POST'])
def register():
    email = request.json.get('email')
    password = request.json.get('password')
    try:
        user = supabase_client.auth.sign_up(email, password)
        return jsonify({'status': 'success', 'user': user}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@app.route('/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')
    try:
        user = supabase_client.auth.sign_in(email, password)
        return jsonify({'status': 'success', 'user': user}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@app.route('/start', methods=['POST'])
def start_game():
    difficulty = request.json.get('difficulty', Difficulty.EASY)
    flappy_dragon_game.difficulty = difficulty
    flappy_dragon_game.reset_game()
    flappy_dragon_game.main()
    return jsonify({"status": "Game started", "difficulty": difficulty})

@app.route('/difficulty', methods=['POST'])
def set_difficulty():
    difficulty = request.json.get('difficulty', Difficulty.EASY)
    flappy_dragon_game.difficulty = difficulty
    flappy_dragon_game.reset_game()
    return jsonify({"status": "Difficulty set", "difficulty": difficulty})

if __name__ == '__main__':
    app.run(debug=False)
