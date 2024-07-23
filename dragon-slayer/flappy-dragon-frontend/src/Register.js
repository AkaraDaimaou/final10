import React, { useState } from 'react';
import axios from 'axios';
import './styles.css';

function Register() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [message, setMessage] = useState('');

    const handleRegister = async () => {
        try {
            const response = await axios.post('http://localhost:5000/register', { email, password });
            setMessage('Registration successful');
        } catch (error) {
            setMessage('Registration failed: ' + error.response.data.message);
        }
    };

    return (
        <div>
            <h2>Register</h2>
            <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Email" />
            <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Password" />
            <button onClick={handleRegister}>Register</button>
            <p>{message}</p>
        </div>
    );
}

export default Register;
