import React from 'react';

const FloatingActionButton = ({ children, onClick, position, icon }) => {
    return (
        <button
            onClick={onClick}
            className={`fixed ${position} z-50 glass-panel p-3 rounded-full text-white hover:bg-indigo-700 transition-all duration-300 ease-in-out transform hover:scale-110 focus:outline-none`}
            aria-label={children}
        >
            {icon}
        </button>
    );
};

export default FloatingActionButton;
