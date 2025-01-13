import React, { useState } from 'react';
import axios from 'axios';
import './Annonce.css';

const Annonce = ({ onAnnonce }) => {
    const values = [80, 90, 100, 110, 120, 130, 140, 150, 160];
    const suits = ['hearts', 'diamonds', 'clubs', 'spades', 'all trump', 'no trump'];

    const [selectedValue, setSelectedValue] = useState(null);
    const [selectedSuit, setSelectedSuit] = useState(null);
    const [isSubmitting, setIsSubmitting] = useState(false);

    const handleValueClick = (value) => {
        setSelectedValue(value);
    };

    const handleSuitClick = (suit) => {
        setSelectedSuit(suit);
    };

    const handleAnnonce = async () => {
        if (selectedValue && selectedSuit && !isSubmitting) {
            setIsSubmitting(true); // Disable further submissions immediately
            const human_annonce = { value: selectedValue, suit: selectedSuit };

            // Notify parent component of the annonce
            onAnnonce(human_annonce);

            try {
                const response = await axios.post('http://localhost:5000/annonce', {
                    human_annonce
                });

                console.log("Annonce result:", response.data);
            } catch (error) {
                console.error("There was an error getting the annonce:", error);
            } finally {
                setIsSubmitting(false); // Re-enable submission
            }
        }
    };

    const handlePass = async () => {
        if (!isSubmitting) {
            setIsSubmitting(true); // Disable further submissions immediately
            const human_annonce = "pass";

            // Notify parent component of the pass
            onAnnonce(human_annonce);

            try {
                const response = await axios.post('http://localhost:5000/annonce', {
                    human_annonce
                });

                console.log("Annonce result:", response.data);
            } catch (error) {
                console.error("There was an error getting the annonce:", error);
            } finally {
                setIsSubmitting(false); // Re-enable submission
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
                        disabled={isSubmitting} // Disable button if a submission is in progress
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
                        disabled={isSubmitting} // Disable button if a submission is in progress
                    >
                        {suit}
                    </button>
                ))}
            </div>
            <button
                onClick={handleAnnonce}
                className="annonce-submit"
                disabled={isSubmitting || !selectedValue || !selectedSuit} // Disable unless valid selection
            >
                Submit Annonce
            </button>
            <button
                onClick={handlePass}
                className="annonce-pass"
                disabled={isSubmitting} // Disable if already submitting
            >
                Pass
            </button>
        </div>
    );
};

export default Annonce;