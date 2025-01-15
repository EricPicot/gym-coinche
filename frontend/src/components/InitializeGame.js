import React, { useState } from 'react';
import axios from 'axios';
import CardTable from './CardTable';
import './CardTable.css';
import BiddingOptions from './BiddingOptions';

const InitializeGame = () => {
    const [playersHands, setPlayersHands] = useState(null);
    const [biddingOptions, setBiddingOptions] = useState([]);
    const [biddingPhaseOver, setBiddingPhaseOver] = useState(false);
    const [isInitialized, setIsInitialized] = useState(false);
    const [timestamp, setTimestamp] = useState(Date.now());
    const [annonces, setAnnonces] = useState({});

    const handleInitialize = async () => {
        try {
            const response = await axios.post('http://localhost:5000/initialize');
            console.log("Response data:", response.data); // Debug log
            setPlayersHands(response.data.players_hands);
            setBiddingOptions(response.data.bidding_options);
            setBiddingPhaseOver(response.data.bidding_phase_over); // Update based on server response
            setAnnonces(response.data.annonces); // Update annonces based on server response
            setIsInitialized(true);
            setTimestamp(Date.now()); // Update timestamp to force re-render
        } catch (error) {
            console.error("There was an error initializing the game:", error);
        }
    };

    const updateAnnonces = (newAnnonces) => {
        setAnnonces(newAnnonces);
    };

    console.log("Game initialized ", `${biddingPhaseOver}`); // Debug log

    return (
        <div>
            <h1>Initialize Game</h1>
            <button onClick={handleInitialize}>Initialize Game</button>
            {isInitialized && (
                <div key={timestamp}>
                    <CardTable playersHands={playersHands} annonces={annonces} biddingPhaseOver={biddingPhaseOver} />
                    <BiddingOptions player="South" options={biddingOptions} biddingPhaseOver={biddingPhaseOver} updateAnnonces={updateAnnonces} />
                </div>
            )}
        </div>
    );
};

export default InitializeGame;