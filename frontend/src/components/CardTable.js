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
                        {playersHands["North"] && playersHands["North"].map((card, index) => (
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
                        {playersHands["West"] && playersHands["West"].map((card, index) => (
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
                        {playersHands["South"] && playersHands["South"].map((card, index) => (
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
                        {playersHands["East"] && playersHands["East"].map((card, index) => (
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