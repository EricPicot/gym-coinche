import React, { useState } from 'react';
import axios from 'axios';
import './Annonce.css';

const Annonce = ({ onAnnonce }) => {
    const values = [80, 90, 100, 110, 120, 130, 140, 150, 160];
    const suits = ['hearts', 'diamonds', 'clubs', 'spades'];

    const [selectedValue, setSelectedValue] = useState(null);
    const [selectedSuit, setSelectedSuit] = useState(null);
    const [currentContractValue, setCurrentContractValue] = useState(80);
    const [currentContractHolder, setCurrentContractHolder] = useState('opponent');

    const handleValueClick = (value) => {
        setSelectedValue(value);
    };

    const handleSuitClick = (suit) => {
        setSelectedSuit(suit);
    };

    const handleAnnonce = async () => {
        if (selectedValue && selectedSuit) {
            const annonce = { value: selectedValue, suit: selectedSuit };
            onAnnonce(annonce);

            try {
                const response = await axios.post('http://localhost:5000/annonce', {
                    player_index: 1,  // Assuming player 1 is making the annonce
                    current_contract_value: currentContractValue,
                    current_contract_holder: currentContractHolder
                });
                console.log("Annonce result:", response.data.annonce);
            } catch (error) {
                console.error("There was an error getting the annonce:", error);
            }
        }
    };

    return (
        <div className="annonce">
            <h2>Annonce Phase</h2>
            <div className="values">
                {values.map((value) => (
                    <button
                        key={value}
                        className={`annonce-button ${selectedValue === value ? 'selected' : ''}`}
                        onClick={() => handleValueClick(value)}
                    >
                        {value}
                    </button>
                ))}
            </div>
            <div className="suits">
                {suits.map((suit) => (
                    <button
                        key={suit}
                        className={`annonce-button ${selectedSuit === suit ? 'selected' : ''}`}
                        onClick={() => handleSuitClick(suit)}
                    >
                        {suit}
                    </button>
                ))}
            </div>
            <button onClick={handleAnnonce} className="annonce-submit">Submit Annonce</button>
        </div>
    );
};

export default Annonce;