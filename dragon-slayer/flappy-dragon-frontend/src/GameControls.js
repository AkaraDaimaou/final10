import React, { useState, useEffect } from 'react';
import axios from 'axios';

function GameControls() {
    const [difficulty, setDifficulty] = useState('EASY');
    const [gameStatus, setGameStatus] = useState('');
    const [username, setUsername] = useState('');
    const [savedUsername, setSavedUsername] = useState('Guest');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const startGame = async () => {
        setLoading(true);
        setError('');
        try {
            const response = await axios.post('http://localhost:5000/start', { difficulty });
            setGameStatus(response.data.status);
        } catch (error) {
            console.error('Error starting the game:', error);
            setError('Failed to start the game. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    const setDifficultyLevel = async (level) => {
        setLoading(true);
        setError('');
        try {
            const response = await axios.post('http://localhost:5000/difficulty', { difficulty: level });
            setDifficulty(level);
            setGameStatus(response.data.status);
        } catch (error) {
            console.error('Error setting difficulty:', error);
            setError('Failed to set difficulty. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    const saveUsername = async () => {
        setLoading(true);
        setError('');
        try {
            const response = await axios.post('http://localhost:5000/save_user', { username });
            setSavedUsername(response.data.username);
        } catch (error) {
            console.error('Error saving username:', error);
            setError('Failed to save username. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    const fetchUsername = async () => {
        setLoading(true);
        setError('');
        try {
            const response = await axios.get('http://localhost:5000/get_user');
            setSavedUsername(response.data.username);
        } catch (error) {
            console.error('Error fetching username:', error);
            setError('Failed to fetch username. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchUsername();
    }, []);

    return (
        <div>
            <h1>Flappy Dragon Game</h1>
            <div>
                <label>
                    Username:
                    <input
                        type="text"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                    />
                </label>
                <button onClick={saveUsername}>Save Username</button>
            </div>
            <button onClick={() => setDifficultyLevel('EASY')}>Easy</button>
            <button onClick={() => setDifficultyLevel('MEDIUM')}>Medium</button>
            <button onClick={() => setDifficultyLevel('HARD')}>Hard</button>
            <button onClick={startGame}>Start Game</button>
            {loading && <p>Loading...</p>}
            {error && <p style={{ color: 'red' }}>{error}</p>}
            <p>Status: {gameStatus}</p>
            <p>Welcome, {savedUsername}!</p>
        </div>
    );
}

export default GameControls;
