import React, { useState } from 'react';

function Register({ switchToLogin, onSignupSuccess }) {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [email, setEmail] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const handleSignup = async () => {
        if (!email || !password || !username) {
            setError('Please fill in all fields.');
            return;
        }

        setLoading(true);
        try {
            // Simulate signup logic
            console.log('Signing up with', username, email, password);

            // Simulate a successful signup
            onSignupSuccess();
        } catch (err) {
            setError('Signup failed. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div>
            <h2>Register</h2>
            <input
                type="text"
                placeholder="Username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
            />
            <input
                type="email"
                placeholder="Email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
            />
            <input
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
            />
            <button onClick={handleSignup} disabled={loading}>
                {loading ? 'Registering...' : 'Sign Up'}
            </button>
            {error && <p>{error}</p>}
            <button onClick={switchToLogin}>Already have an account? Log in</button>
        </div>
    );
}

export default Register;
