const express = require('express');
const http = require('http');
const { Server } = require('socket.io');
const { createClient } = require('@supabase/supabase-js');

const app = express();
const server = http.createServer(app);
const io = new Server(server);

const supabaseUrl = 'your_supabase_url';
const supabaseKey = 'your_supabase_key';
const supabase = createClient(supabaseUrl, supabaseKey);

app.use(express.json());

let gameState = {
    players: {},
    enemies: [],
    platforms: [],  // Add platforms to the game state
    collectibles: [],  // Add collectibles to the game state
    powerups: []  // Add power-ups to the game state
};

const saveGameState = async () => {
    const { data, error } = await supabase
        .from('game_states')
        .upsert({ id: 1, state: gameState });

    if (error) console.error(error);
};

const loadGameState = async () => {
    const { data, error } = await supabase
        .from('game_states')
        .select('state')
        .eq('id', 1)
        .single();

    if (error) {
        console.error(error);
    } else {
        gameState = data.state;
        io.emit('gameState', gameState);
    }
};

// Load game state on server start
loadGameState();

io.on('connection', (socket) => {
    console.log('a user connected', socket.id);
    gameState.players[socket.id] = { x: 100, y: 100, score: 0 };

    socket.emit('gameState', gameState);

    socket.on('playerMove', (data) => {
        gameState.players[socket.id] = { ...gameState.players[socket.id], ...data };
        io.emit('gameState', gameState);
        saveGameState();
    });

    socket.on('disconnect', () => {
        console.log('user disconnected', socket.id);
        delete gameState.players[socket.id];
        io.emit('gameState', gameState);
        saveGameState();
    });
});

const PORT = process.env.PORT || 5000;
server.listen(PORT, () => console.log(`Server running on port ${PORT}`));
