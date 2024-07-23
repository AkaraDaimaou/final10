import React, { useEffect, useState } from 'react';
import io from 'socket.io-client';
import './Multiplayer.css';

const socket = io('http://localhost:5000');

function Multiplayer() {
    const [playerName, setPlayerName] = useState('');
    const [score, setScore] = useState(0);
    const [challenge, setChallenge] = useState('');
    const [opponentScore, setOpponentScore] = useState(0);
    const [isChallenged, setIsChallenged] = useState(false);
    const [player1, setPlayer1] = useState({ name: '', score: 0 });
    const [player2, setPlayer2] = useState({ name: '', score: 0 });

    useEffect(() => {
        socket.on('challenge', (opponent) => {
            setChallenge(opponent);
            setIsChallenged(true);
        });

        socket.on('scoreUpdate', ({ playerId, score }) => {
            if (playerId !== socket.id) {
                setOpponentScore(score);
                setPlayer2((prev) => ({ ...prev, score }));
            }
        });

        return () => {
            socket.off('challenge');
            socket.off('scoreUpdate');
        };
    }, []);

    const registerPlayer = () => {
        socket.emit('register', playerName);
        setPlayer1({ name: playerName, score });
    };

    const updateScore = () => {
        socket.emit('updateScore', score);
        setPlayer1((prev) => ({ ...prev, score }));
    };

    return (
        <div>
            <h1>Multiplayer Game</h1>
            <input
                type="text"
                placeholder="Enter your name"
                value={playerName}
                onChange={(e) => setPlayerName(e.target.value)}
            />
            <button onClick={registerPlayer}>Register</button>
            <button onClick={updateScore}>Update Score</button>
            {isChallenged && <p>Challenge from {challenge}!</p>}
            <div className="split-screen">
                <div className="player-screen player1">
                    <h2>Player 1: {player1.name}</h2>
                    <div className="game-canvas">{/* Player 1's game */}</div>
                    <p>Score: {player1.score}</p>
                </div>
                <div className="player-screen player2">
                    <h2>Player 2: {player2.name}</h2>
                    <div className="game-canvas">{/* Player 2's game */}</div>
                    <p>Score: {player2.score}</p>
                </div>
            </div>
        </div>
    );
}

export default Multiplayer;
