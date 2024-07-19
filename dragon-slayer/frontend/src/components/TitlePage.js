import React from 'react';
import { useNavigate } from 'react-router-dom';
import titleImage from '../assets/title-image.png'; 
import pressEnterText from '../assets/press-enter-text.png'; 

const TitlePage = () => {
    const navigate = useNavigate();

    const handleStart = () => {
        navigate('/menu');
    };

    return (
        <div>
            <img src={titleImage} alt="Dragon Slayer" />
            <button onClick={handleStart}>
                <img src={pressEnterText} alt="Press Enter" />
            </button>
        </div>
    );
};

export default TitlePage;
