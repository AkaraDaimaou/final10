import React, { useState } from 'react';
import Register from './Register';
import Login from './Login';

function App() {
    const [isRegistering, setIsRegistering] = useState(true);

    return (
        <div>
            <h1>Game</h1>
            {isRegistering ? (
                <Register switchToLogin={() => setIsRegistering(false)} />
            ) : (
                <Login switchToRegister={() => setIsRegistering(true)} />
            )}
            <button onClick={() => setIsRegistering(!isRegistering)}>
                {isRegistering ? 'Already have an account? Log in' : 'New user? Register'}
            </button>
        </div>
    );
}

export default App;
