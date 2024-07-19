import React from 'react';
import { useNavigate } from 'react-router-dom';

const MainMenu = () => {
    const navigate = useNavigate();

    const handleSinglePlayer = () => {
        navigate('/game');
    };

    const handleMultiplayer = () => {
        navigate('/multiplayer');
    };

    const handleSettings = () => {
        // Implement settings functionality
    };

    const handleExit = () => {
        // Implement exit functionality
    };

    return (
        <div>
            <h1>Main Menu</h1>
            <button onClick={handleSinglePlayer}>Single Player</button>
            <button onClick={handleMultiplayer}>Multiplayer</button>
            <button onClick={handleSettings}>Settings</button>
            <button onClick={handleExit}>Exit</button>
        </div>
    );
};

export default MainMenu;
