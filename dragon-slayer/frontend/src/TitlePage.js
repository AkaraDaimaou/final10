import React from 'react';
import { useHistory } from 'react-router-dom';

const TitlePage = () => {
    const history = useHistory();

    const handleStart = () => {
        history.push('/menu');
    };

    return (
        <div>
            <h1>Dragon Slayer</h1>
            <button onClick={handleStart}>Start Game</button>
        </div>
    );
};

export default TitlePage;
