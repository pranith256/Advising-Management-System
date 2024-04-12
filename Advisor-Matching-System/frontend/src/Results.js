import React from 'react';
import './Results.css';
import Illini from './e1b8be88-4225-49c9-ac3c-fda3d7dbb3d5.jpg';

const Results = ({ profData, setHome, showResultsPage }) => {

  const handleSubmit = (e) => {
    e.preventDefault();
    setHome(true);  
    showResultsPage(false);
  };

  return (
    <div className="results-container">
      <img src={Illini} alt="Descriptive Alt Text" className="form-image" />
      <h1>The top 5 professors that would be a great fit as your advisors are:</h1>
      <div className="cards-container">
        {profData.map((prof, index) => (
          <a href={prof.website} target="_blank" rel="noopener noreferrer" key={index} className="prof-link">
          <div key={index} className="prof-card">
            <img src={prof.image} alt={`Professor ${prof.profname}`} className="professor-image" />
            <p>{prof.profname}</p>
          </div>
          </a>
        ))}
      </div>
      <button className="more-info-btn" onClick={handleSubmit} >Go Back Home</button>
    </div>
  );
};

export default Results;
