import React, { useRef, useEffect } from 'react';
import playerImage from '../assets/player.png';
import enemyImage from '../assets/enemy.png';
import platformImage from '../assets/platform.png';

const Game = () => {
    const canvasRef = useRef(null);

    useEffect(() => {
        const canvas = canvasRef.current;
        const ctx = canvas.getContext('2d');

        const player = new Image();
        player.src = playerImage;

        const enemy = new Image();
        enemy.src = enemyImage;

        const platform = new Image();
        platform.src = platformImage;

        player.onload = () => {
            ctx.drawImage(player, 100, 100, 50, 50);
        };

        enemy.onload = () => {
            ctx.drawImage(enemy, 400, 100, 50, 50);
        };

        platform.onload = () => {
            ctx.drawImage(platform, 200, 500, 400, 20);
            ctx.drawImage(platform, 100, 400, 200, 20);
            ctx.drawImage(platform, 400, 300, 200, 20);
        };
    }, []);

    return (
        <div>
            <canvas ref={canvasRef} width="800" height="600"></canvas>
        </div>
    );
};

export default Game;
