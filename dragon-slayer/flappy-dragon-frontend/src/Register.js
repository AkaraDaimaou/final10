import React, { useState } from 'react';
import { supabase } from './supabaseClient';

function Register({ switchToLogin }) {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [email, setEmail] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const register = async () => {
        if (!email || !password || !username) {
            setError('Please fill in all fields.');
            return;
        }

        setLoading(true);
        try {
            const { data, error } = await supabase.auth.signUp({
                email,
                password,
                options: {
                    data: { username }
                }
            });
            if (error) {
                setError(error.message);
            } else {
                console.log(data);
                // You could add a redirect or show a success message here
            }
        } catch (error) {
            setError('Registration failed. Please try again.');
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
            <button onClick={register} disabled={loading}>
                {loading ? 'Registering...' : 'Register'}
            </button>
            {error && <p>{error}</p>}
            <button onClick={switchToLogin}>Already have an account? Log in</button>
        </div>
    );
}

export default Register;
