import React from 'react';
import Register from './Register';  // Correct import for Register component
import Login from './Login';        // Correct import for Login component
import GameControls from './GameControls';

function App() {
    return (
        <div>
            <Register />
            <Login />
            <GameControls />
        </div>
    );
}

export default App;