import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import TitlePage from './components/TitlePage';
import MainMenu from './components/MainMenu';
import Game from './components/Game';
import Multiplayer from './components/Multiplayer';
import Settings from './components/Settings';

const App = () => {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<TitlePage />} />
                <Route path="/menu" element={<MainMenu />} />
                <Route path="/game" element={<Game />} />
                <Route path="/multiplayer" element={<Multiplayer />} />
                <Route path="/settings" element={<Settings />} />
            </Routes>
        </Router>
    );
};

export default App;
