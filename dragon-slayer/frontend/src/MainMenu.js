import React from 'react';
import { useHistory } from 'react-router-dom';

const MainMenu = () => {
    const history = useHistory();

    const handleSinglePlayer = () => {
        history.push('/game');
    };

    const handleMultiplayer = () => {
        history.push('/multiplayer');
    };

    return (
        <div>
            <h1>Main Menu</h1>
            <button onClick={handleSinglePlayer}>Single Player</button>
            <button onClick={handleMultiplayer}>Multiplayer</button>
        </div>
    );
};

export default MainMenu;
