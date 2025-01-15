import React, { useState, useEffect } from 'react';

const BiddingOptions = ({ player, options: initialOptions, biddingPhaseOver: parentBiddingPhaseOver, updateAnnonces }) => {
    const [options, setOptions] = useState(initialOptions);
    const [selectedValue, setSelectedValue] = useState(null);
    const [selectedSuit, setSelectedSuit] = useState(null);
    const [biddingPhaseOver, setBiddingPhaseOver] = useState(parentBiddingPhaseOver);

    // Update biddingPhaseOver state when parentBiddingPhaseOver prop changes
    useEffect(() => {
        setBiddingPhaseOver(parentBiddingPhaseOver);
    }, [parentBiddingPhaseOver]);

    const fetchBiddingOptions = () => {
        console.log('Fetching bidding options for player:', player);
        fetch(`http://localhost:5000/get_bidding_options?player=${player}`)
            .then((response) => response.json())
            .then((data) => {
                console.log('Fetched options:', data.options);
                setOptions(data.options); // Update options
                setBiddingPhaseOver(data.bidding_phase_over); // Update bidding phase status from fetch
                updateAnnonces(data.annonces); // Update annonces from fetch
            })
            .catch((error) => {
                console.error('Error fetching bidding options:', error);
            });
    };

    // Trigger fetchBiddingOptions at the beginning
    useEffect(() => {
        fetchBiddingOptions();
    }, []);

    useEffect(() => {
        fetchBiddingOptions(); // Fetch options when the component mounts or player changes
    }, [player]);

    const sendBid = (bid) => {
        console.log('Sending bid:', bid);
        fetch('http://localhost:5000/bid', {
            method: 'POST',
            mode: 'cors',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ player: player, bid: bid }),
        })
            .then((response) => response.json())
            .then((data) => {
                if (data.status === 'success') {
                    console.log('Bid successful, fetching new options');
                    fetchBiddingOptions(); // Fetch new options after a successful bid
                }
            })
            .catch((error) => {
                console.error('Error sending bid:', error);
            });
    };

    const handleValueClick = (value) => {
        setSelectedValue(value);
    };

    const handleSuitClick = (suit) => {
        setSelectedSuit(suit);
    };

    const handlePassClick = () => {
        setSelectedValue(null);
        setSelectedSuit(null);
        sendBid('pass');
    };

    const handleMakeBiddingClick = () => {
        if (selectedValue && selectedSuit) {
            sendBid(`${selectedValue} of ${selectedSuit}`);
        } else {
            console.log('Please select both a value and a suit before making a bid.');
        }
    };

    console.log('biddingPhaseOver:', biddingPhaseOver);

    if (biddingPhaseOver) {
        return null; // Don't render anything if the bidding phase is over
    }

    console.log('Rendering bidding options:', options);

    const values = [...new Set(options.map((option) => option.split(' ')[0]))];
    const suits = ['hearts', 'spades', 'diamonds', 'clubs'];

    return (
        <div className="bidding-options">
            <div>
                <h3>Values</h3>
                {values.map((value) => (
                    <button key={value} onClick={() => handleValueClick(value)}>
                        {value}
                    </button>
                ))}
            </div>
            <div>
                <h3>Suits</h3>
                {suits.map((suit) => (
                    <button key={suit} onClick={() => handleSuitClick(suit)}>
                        {suit}
                    </button>
                ))}
            </div>
            <div>
                <h3>Other</h3>
                <button onClick={handlePassClick}>Pass</button>
                <button onClick={handleMakeBiddingClick}>Make Bidding</button>
            </div>
        </div>
    );
};

export default BiddingOptions;