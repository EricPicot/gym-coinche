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

    const handleAnnonce = (annonce) => {
        console.log("Annonce submitted:", annonce);
        // You can send the annonce to the backend or handle it as needed
    };

    return (
        <div>
            <h1>Initialize Game</h1>
            <button onClick={handleInitialize}>Initialize Game</button>
            {playersHands && (
                <div>
                    <CardTable playersHands={playersHands} onAnnonce={handleAnnonce} />
                </div>
            )}
        </div>
    );
};

export default InitializeGame;