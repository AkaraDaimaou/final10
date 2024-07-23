import React, { useState } from 'react';
import Register from './Register';
import Login from './Login';
import Confirmation from './Confirmation';

function App() {
    const [isRegistering, setIsRegistering] = useState(true);
    const [isConfirmed, setIsConfirmed] = useState(false);

    return (
        <div>
            <h1>Game</h1>
            {isConfirmed ? (
                <Confirmation />
            ) : isRegistering ? (
                <Register switchToLogin={() => setIsRegistering(false)} onSignupSuccess={() => setIsConfirmed(true)} />
            ) : (
                <Login switchToRegister={() => setIsRegistering(true)} />
            )}
            {!isConfirmed && (
                <button onClick={() => setIsRegistering(!isRegistering)}>
                    {isRegistering ? 'Already have an account? Log in' : 'New user? Register'}
                </button>
            )}
        </div>
    );
}

export default App;
