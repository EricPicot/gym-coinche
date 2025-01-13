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

    const handleAnnonce = (human_annonce) => {
        console.log("Annonce submitted:", human_annonce);
        // Send the annonce to the backend
        axios.post('http://localhost:5000/annonce', { human_annonce })
            .then(response => {
                console.log("Annonce result:", response.data);
            })
            .catch(error => {
                console.error("There was an error getting the annonce:", error);
            });
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