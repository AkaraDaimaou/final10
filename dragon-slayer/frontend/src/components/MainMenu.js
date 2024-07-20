// src/components/MainMenu.js
import React from 'react';
import { useNavigate } from 'react-router-dom';

const MainMenu = () => {
    const navigate = useNavigate();

    return (
        <div className="main-menu">
            <h1>Main Menu</h1>
            <button onClick={() => navigate('/game')}>Start Game</button>
            <button onClick={() => navigate('/settings')}>Settings</button>
            <button onClick={() => window.close()}>Exit</button>
        </div>
    );
};

export default MainMenu;
