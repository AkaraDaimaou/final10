import React, { useEffect, useState } from 'react';
import { io } from 'socket.io-client';

const Multiplayer = () => {
    const [players, setPlayers] = useState({});
    const socket = io('http://localhost:5000');

    useEffect(() => {
        socket.on('gameState', (gameState) => {
            setPlayers(gameState.players);
        });

        return () => {
            socket.disconnect();
        };
    }, [socket]);

    const handleKeyPress = (e) => {
        const data = { x: 100, y: 100 };
        if (e.key === 'ArrowLeft') {
            data.x -= 5;
        }
        if (e.key === 'ArrowRight') {
            data.x += 5;
        }
        if (e.key === 'ArrowUp') {
            data.y -= 5;
        }
        if (e.key === 'ArrowDown') {
            data.y += 5;
        }
        socket.emit('playerMove', data);
    };

    useEffect(() => {
        window.addEventListener('keydown', handleKeyPress);
        return () => {
            window.removeEventListener('keydown', handleKeyPress);
        };
    }, []);

    return (
        <div>
            <h2>Multiplayer Component</h2>
            <div>
                {Object.keys(players).map((id) => (
                    <div key={id}>
                        Player {id}: {players[id].x}, {players[id].y} | Score: {players[id].score}
                    </div>
                ))}
            </div>
        </div>
    );
};

export default Multiplayer;
