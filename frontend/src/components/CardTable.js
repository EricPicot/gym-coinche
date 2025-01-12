import React from 'react';
import './CardTable.css';
import Annonce from './Annonce';

const CardTable = ({ playersHands, onAnnonce }) => {
    const getCardImage = (card) => {
        const [value, suit] = card.split(' of ');
        return `/cards/${value}_of_${suit}.png`;
    };

    return (
        <div className="card-table">
            {playersHands && (
                <>
                    <div className="player north">
                        {playersHands["Player 3"] && playersHands["Player 3"].map((card, index) => (
                            <div key={index} className="card rotated">
                                <img
                                    src={getCardImage(card)}
                                    alt={card}
                                    className="card-image"
                                />
                            </div>
                        ))}
                    </div>
                    <div className="player west">
                        {playersHands["Player 2"] && playersHands["Player 2"].map((card, index) => (
                            <div key={index} className="card rotated-left">
                                <img
                                    src={getCardImage(card)}
                                    alt={card}
                                    className="card-image"
                                />
                            </div>
                        ))}
                    </div>
                    <div className="player south">
                        {playersHands["Player 1"] && playersHands["Player 1"].map((card, index) => (
                            <div key={index} className="card">
                                <img
                                    src={getCardImage(card)}
                                    alt={card}
                                    className="card-image"
                                />
                            </div>
                        ))}
                    </div>
                    <div className="annonce-container">
                        <Annonce onAnnonce={onAnnonce} />
                    </div>
                    <div className="player east">
                        {playersHands["Player 0"] && playersHands["Player 0"].map((card, index) => (
                            <div key={index} className="card rotated-right">
                                <img
                                    src={getCardImage(card)}
                                    alt={card}
                                    className="card-image"
                                />
                            </div>
                        ))}
                    </div>
                </>
            )}
        </div>
    );
};

export default CardTable;