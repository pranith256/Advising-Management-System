import React, { useState, useEffect } from 'react';
import './App.css';
import AdvisorMatchingForm from './AdvisorMatchingForm';
import Results from './Results';
import Loader from './Loader';

function App() {

  const [profData, setProfData] = useState({});
  const [showResults, showResultsPage] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [isHome, setHome] = useState(true);


  const handleProfData = (data) => {
    setProfData(data);
  }

  return (
    <div className="App">
      {!isLoading && isHome && <AdvisorMatchingForm showResultsPage={showResultsPage} handleProfData={handleProfData} setIsLoading={setIsLoading} setHome={setHome}/> }
      {!isLoading && showResults &&
      <div className='results'>
        <Results profData = {[
                        {"profname": profData[0][0], "image": profData[0][1], "website": profData[0][2]},
                        {"profname": profData[1][0], "image": profData[1][1], "website": profData[1][2]},
                        {"profname": profData[2][0], "image": profData[2][1], "website": profData[2][2]},
                        {"profname": profData[3][0], "image": profData[3][1], "website": profData[3][2]},
                        {"profname": profData[4][0], "image": profData[4][1], "website": profData[4][2]}
                        ]
                      } setHome={setHome} showResultsPage={showResultsPage} />
      </div> }
      {isLoading && <Loader /> }
    </div>
  );
}

export default App;
