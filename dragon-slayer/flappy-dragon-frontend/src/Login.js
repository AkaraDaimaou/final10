import React, { useState } from 'react';
import axios from 'axios';
import { supabase } from './supabaseClient';
import './styles.css';

function Login() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [message, setMessage] = useState('');
    const [user, setUser] = useState(null);

    const handleLogin = async () => {
        try {
            const response = await axios.post('http://localhost:5000/login', { email, password });
            setMessage('Login successful');
            setUser(response.data.user);
        } catch (error) {
            setMessage('Login failed: ' + error.response.data.message);
        }
    };

    return (
        <div>
            <h2>Login</h2>
            <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Email" />
            <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Password" />
            <button onClick={handleLogin}>Login</button>
            <p>{message}</p>
            {user && <p>Welcome, {user.user_metadata.full_name || 'User'}!</p>}
        </div>
    );
}

export default Login;
