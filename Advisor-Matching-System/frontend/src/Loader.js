import React from 'react';
import './Loader.css';

const Loader = () => {
  return (
    <div className="loader-container">
      <p className="loading-message">Please wait while we fetch your potential advisors</p>
      <div className="progress-bar"></div>
      {/* Added message */}
    </div>
  );
};


export default Loader;
