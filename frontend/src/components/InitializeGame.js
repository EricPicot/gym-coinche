import React, { useState } from 'react';
import axios from 'axios';
import CardTable from './CardTable';
import './CardTable.css';

const InitializeGame = () => {
    const [playersHands, setPlayersHands] = useState(null);

    const handleInitialize = async () => {
        try {
            const response = await axios.post('http://localhost:5000/initialize');
            console.log("Response data:", response.data); // Debug log
            setPlayersHands(response.data);
        } catch (error) {
            console.error("There was an error initializing the game:", error);
        }
    };

    return (
        <div>
            <h1>Initialize Game</h1>
            <button onClick={handleInitialize}>Initialize Game</button>
            {playersHands && (
                <div>
                    <CardTable playersHands={playersHands} />
                </div>
            )}
        </div>
    );
};

export default InitializeGame;