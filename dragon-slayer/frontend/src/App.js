import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import TitlePage from './components/TitlePage';
import MainMenu from './components/MainMenu';
import Game from './components/Game';
import Multiplayer from './components/Multiplayer';

const App = () => {
    return (
        <Router>
            <Switch>
                <Route path="/" exact component={TitlePage} />
                <Route path="/menu" component={MainMenu} />
                <Route path="/game" component={Game} />
                <Route path="/multiplayer" component={Multiplayer} />
            </Switch>
        </Router>
    );
};

export default App;
