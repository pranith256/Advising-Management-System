import React, { useState } from 'react';
import './AdvisorMatching.css';
import Illini from './e1b8be88-4225-49c9-ac3c-fda3d7dbb3d5.jpg'; 


const AdvisorMatchingForm = ({handleProfData, showResultsPage, setIsLoading, setHome}) => {
  const [formData, setFormData] = useState({
    researchInterests: '',
    paperTitles: '',
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log(formData);
    setIsLoading(true);
   
    setTimeout(() => {
      const studentData = {
        "researchInterests": formData.researchInterests,
        "paperTitles": formData.paperTitles
      }
      async function postData() {
        try {
          const response = await fetch('http://localhost:5000/api/student', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(studentData),
          });
      
          if (response.ok) {
            const data = await response.json();
            console.log(data);
            console.log('Success in fetching the professors data');
            handleProfData(data);
            setHome(false);
            showResultsPage(true);
          } else {
            console.log('Error', response.status);
          }
        } catch (error) {
          console.error('Fetch error:', error);
        } finally {
          setIsLoading(false); 
        }
      }
      
       postData();
          }, 5000); 

  };

  return (
    <div className="form-container">
      <img src={Illini} alt="Descriptive Alt Text" className="form-image" />
      <div><h1 className="page-title">Advisor Matching System for CS CSULB Students</h1></div>
      <form onSubmit={handleSubmit} className="advisor-matching-form">
        <p>Please enter your research interests and paper titles in the fields below. These will be used to match you with potential advisors.</p>
        
        <textarea
          name="researchInterests"
          value={formData.researchInterests}
          onChange={handleChange}
          placeholder="Enter your research interests here"
          className="form-textarea"
        />
        
        <textarea
          name="paperTitles"
          value={formData.paperTitles}
          onChange={handleChange}
          placeholder="Enter research paper titles here"
          className="form-textarea"
        />

        <button className = "submit-btn" onClick={handleSubmit}>Submit</button>
        
      </form>
    </div>
    
    
  );
};

export default AdvisorMatchingForm;
