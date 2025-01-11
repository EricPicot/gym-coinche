import React, { useState } from 'react';
import axios from 'axios';

const Annonce = () => {
    const [gameState, setGameState] = useState('');
    const [annonce, setAnnonce] = useState(null);

    const handleAnnonce = async () => {
        const response = await axios.post('http://localhost:5000/annonce', { game_state: gameState });
        setAnnonce(response.data.annonce);
    };

    return (
        <div>
            <h1>Annonce Phase</h1>
            <textarea value={gameState} onChange={(e) => setGameState(e.target.value)} placeholder="Enter game state"></textarea>
            <button onClick={handleAnnonce}>Get Annonce</button>
            {annonce && <div><h2>Annonce:</h2><p>{annonce}</p></div>}
        </div>
    );
};

export default Annonce;