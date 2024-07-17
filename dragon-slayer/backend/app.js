const express = require('express');
const http = require('http');
const { Server } = require('socket.io');
const { createClient } = require('@supabase/supabase-js');

const app = express();
const server = http.createServer(app);
const io = new Server(server);

const supabaseUrl = 'https://bmzebewzxpnheeuhuplh.supabase.co'
const supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJtemViZXd6eHBuaGVldWh1cGxoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjExNzg0MzQsImV4cCI6MjAzNjc1NDQzNH0.sWY8GLXn2-8MMzNpYYShXejONE9qYWhRuW0IivQX2GM'
const supabase = createClient(supabaseUrl, supabaseKey)

app.use(express.json());

let gameState = {
    players: {},
    enemies: [],
};

const saveGameState = async () => {
    const { data, error } = await supabase
        .from('game_states')
        .upsert({ id: 1, state: gameState }, { onConflict: 'id' });

    if (error) console.error('Error saving game state:', error);
};

const loadGameState = async () => {
    const { data, error } = await supabase
        .from('game_states')
        .select('state')
        .eq('id', 1)
        .single();

    if (error) {
        console.error('Error loading game state:', error);
    } else if (data) {
        gameState = data.state;
        io.emit('gameState', gameState);
    }
};

// Load game state on server start
loadGameState();

// Save game state periodically
setInterval(saveGameState, 10000);

io.on('connection', (socket) => {
    console.log('a user connected', socket.id);
    gameState.players[socket.id] = { x: 100, y: 100 };

    socket.emit('gameState', gameState);

    socket.on('playerMove', (data) => {
        gameState.players[socket.id] = data;
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
