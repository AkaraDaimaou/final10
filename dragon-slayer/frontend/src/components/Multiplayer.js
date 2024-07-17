import React, { useEffect, useState, useRef } from 'react';
import { io } from 'socket.io-client';
import playerImage from '../assets/player.png';
import enemyImage from '../assets/enemy.png';
import platformImage from '../assets/platform.png';

const Multiplayer = () => {
    const [players, setPlayers] = useState({});
    const canvasRef = useRef(null);
    const socket = io('http://localhost:5000');

    useEffect(() => {
        socket.on('gameState', (gameState) => {
            setPlayers(gameState.players);
            drawGame(gameState);
        });

        return () => {
            socket.disconnect();
        };
    }, [socket]);

    const drawGame = (gameState) => {
        const canvas = canvasRef.current;
        const ctx = canvas.getContext('2d');

        ctx.clearRect(0, 0, canvas.width, canvas.height);

        Object.keys(gameState.players).forEach(id => {
            const player = new Image();
            player.src = playerImage;
            ctx.drawImage(player, gameState.players[id].x, gameState.players[id].y, 50, 50);
        });

        const enemy = new Image();
        enemy.src = enemyImage;
        ctx.drawImage(enemy, 400, 100, 50, 50);

        const platform = new Image();
        platform.src = platformImage;
        ctx.drawImage(platform, 200, 500, 400, 20);
        ctx.drawImage(platform, 100, 400, 200, 20);
        ctx.drawImage(platform, 400, 300, 200, 20);
    };

    const handleKeyPress = (e) => {
        let data = { x: players[socket.id]?.x || 100, y: players[socket.id]?.y || 100 };
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
    }, [players]);

    return (
        <div>
            <canvas ref={canvasRef} width="800" height="600"></canvas>
        </div>
    );
};

export default Multiplayer;
