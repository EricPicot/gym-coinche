import React from 'react';
import './CardTable.css';

const CardTable = ({ playersHands, annonces, biddingPhaseOver }) => {
    const getCardImage = (card) => {
        const [value, suit] = card.split(' of ');
        return `/cards/${value}_of_${suit}.png`;
    };
    console.log('biddingPhaseOver:', `${biddingPhaseOver}`);

    return (
        <div className="card-table">
            {playersHands && (
                <>
                    <div className="player north">
                        <div className="annonce">{annonces["North"]}</div>
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
                        <div className="annonce">{annonces["West"]}</div>
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
                    <div className="player east">
                        <div className="annonce">{annonces["East"]}</div>
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
                    <div className="player south">
                        <div className="annonce">{annonces["South"]}</div>
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
                </>
            )}
        </div>
    );
};

export default CardTable;