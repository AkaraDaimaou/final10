import React, { useState } from 'react';
import axios from 'axios';

function GameControls() {
    const [difficulty, setDifficulty] = useState('EASY');
    const [gameStatus, setGameStatus] = useState('');

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

    return (
        <div>
            <h1>Flappy Dragon Game</h1>
            <button onClick={() => setDifficultyLevel('EASY')}>Easy</button>
            <button onClick={() => setDifficultyLevel('MEDIUM')}>Medium</button>
            <button onClick={() => setDifficultyLevel('HARD')}>Hard</button>
            <button onClick={startGame}>Start Game</button>
            <p>Status: {gameStatus}</p>
        </div>
    );
}

export default GameControls;
