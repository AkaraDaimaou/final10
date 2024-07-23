const express = require('express');
const http = require('http');
const socketIo = require('socket.io');

const app = express();
const server = http.createServer(app);
const io = socketIo(server);

let players = {}; // { socketId: { playerName, score } }
let waitingPlayer = null;

io.on('connection', (socket) => {
    console.log(`Player connected: ${socket.id}`);

    // Register player
    socket.on('register', (playerName) => {
        players[socket.id] = { playerName, score: 0 };
        if (waitingPlayer) {
            // Pair players
            io.to(socket.id).emit('challenge', waitingPlayer.playerName);
            io.to(waitingPlayer.socketId).emit('challenge', players[socket.id].playerName);
            waitingPlayer = null;
        } else {
            waitingPlayer = { socketId: socket.id, playerName: players[socket.id].playerName };
        }
    });

    // Update score
    socket.on('updateScore', (score) => {
        if (players[socket.id]) {
            players[socket.id].score = score;
            // Notify opponent
            for (let id in players) {
                if (id !== socket.id) {
                    io.to(id).emit('scoreUpdate', { playerId: socket.id, score });
                }
            }
        }
    });

    socket.on('disconnect', () => {
        console.log(`Player disconnected: ${socket.id}`);
        delete players[socket.id];
        if (waitingPlayer && waitingPlayer.socketId === socket.id) {
            waitingPlayer = null;
        }
    });
});

server.listen(5000, () => {
    console.log('Server listening on port 5000');
});
