import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { supabase } from './supabaseClient'; // Your Supabase client
import io from 'socket.io-client';

const socket = io('http://localhost:5000'); // Update with your server address if different

function GameControls() {
    const [difficulty, setDifficulty] = useState('EASY');
    const [gameStatus, setGameStatus] = useState('');
    const [userId, setUserId] = useState(null); // Assuming user ID is available after login
    const [score, setScore] = useState(0); // Track score
    const [level, setLevel] = useState(1); // Track level

    useEffect(() => {
        const fetchUserId = async () => {
            try {
                const { data: { user } } = await supabase.auth.getUser();
                setUserId(user.id);
            } catch (error) {
                console.error('Error fetching user ID:', error);
            }
        };
        fetchUserId();

        socket.on('connect', () => {
            console.log('Connected to server');
        });

        socket.on('disconnect', () => {
            console.log('Disconnected from server');
        });

        return () => {
            socket.off('connect');
            socket.off('disconnect');
        };
    }, []);

    const startGame = async () => {
        try {
            const response = await axios.post('http://localhost:5000/start', { difficulty });
            setGameStatus(response.data.status);
        } catch (error) {
            console.error('Error starting the game:', error);
        }
    };

    const setDifficultyLevel = async (level) => {
        try {
            const response = await axios.post('http://localhost:5000/difficulty', { difficulty: level });
            setDifficulty(level);
            setGameStatus(response.data.status);
        } catch (error) {
            console.error('Error setting difficulty:', error);
        }
    };

    const saveGameData = async (type) => {
        if (!userId) return;
        
        const url = type === 'progress' ? 'http://localhost:5000/save-progress' : 'http://localhost:5000/save-highscore';
        const data = type === 'progress' ? { user_id: userId, level, score } : { user_id: userId, score };

        try {
            const response = await axios.post(url, data);
            console.log(`${type.charAt(0).toUpperCase() + type.slice(1)} saved:`, response.data);
        } catch (error) {
            console.error(`Error saving ${type} to backend:`, error);
        }
    };

    const handleGameEnd = () => {
        saveGameData('progress');
        saveGameData('highscore');
    };

    // Function to update game score using socket
    const updateGame = (newScore) => {
        setScore(newScore);
        socket.emit('game_update', { userId, score: newScore });
    };

    return (
        <div>
            <h1>Flappy Dragon Game</h1>
            <button onClick={() => setDifficultyLevel('EASY')}>Easy</button>
            <button onClick={() => setDifficultyLevel('MEDIUM')}>Medium</button>
            <button onClick={() => setDifficultyLevel('HARD')}>Hard</button>
            <button onClick={startGame}>Start Game</button>
            <button onClick={handleGameEnd}>End Game</button>
            <p>Status: {gameStatus}</p>
        </div>
    );
}

export default GameControls;
