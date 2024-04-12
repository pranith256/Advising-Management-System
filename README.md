# Advising-Management-System

In this journey as a student I have found that approaching a potential advisor to guide the students in their desired path is a challenge. To overcome this chalenge, we have built a advising system which will give a list of advisor based on the shared research interests of the tudents.
Then the model takes advantage of web scraping to gather data of professors which include names, titles, images,, links and research papers published.

# Functionality :
The core functionality is that user inputs their interests, project titles and keywords through the user interface.
Then, the model built using TF-IDF and BM25 algorithms will find the recommended advicors from the scraped data.
The project is build using React for Front end, flask for integration of backend

# Process:
● User Input:
 Users input their research interests through the UI, providing keywords or
sentences that reflect their areas of interest.
● Matching Process:
The system processes user input using TF-IDF and BM25 algorithms.
Professors with the highest similarity scores are identified and presented
as potential advisors.
● Results Display:
 The system displays matched professors along with relevant details, such
as names, images, and links to their webpage.
Users can explore further details and make informed decisions about
potential advisors.

# Setting up Environment :
Install python on VS code

# Running Front-end :
npm install - to install the node-modules
npm start - runs the application on port 3000

# Running Vackend : 
cd to the server /folder
python server.py - runs application on port 5000

