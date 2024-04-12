# pip install scikit-learn Flask Flask-Cors rank-bm25
# python3 server.py

import json
from rank_bm25 import BM25Okapi
import numpy as np
from flask import Flask, jsonify, request
from flask_cors import CORS
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def getSimilarity(student_interests):
    with open('FinalProfessorsData.json', 'r') as file:
        combined_data = json.load(file)

    # Combine interests and publications for each professor
    combined = []
    for key, value in combined_data.items():
        interests = " ".join(value["interests"])
        publications = " ".join([pub["title"] + " " + pub["snippet"] for pub in value.get("publications", [])])
        combined.append(interests + " " + publications)

    # Vectorize with BM25
    tokenized_texts = [doc.split(" ") for doc in combined]
    bm25 = BM25Okapi(tokenized_texts)

    # Calculate similarity
    student_query_tokens = student_interests.split(" ")
    similarities = bm25.get_scores(student_query_tokens)

    # Find the top 5 professors with the highest similarity
    top_matches_indices = np.argsort(similarities)[-5:][::-1]
    
    # Retrieve the top matches with their photo and URL
    top_matches_professors = []
    for i in top_matches_indices:
        prof_key = list(combined_data.keys())[i]
        prof_data = combined_data[prof_key]
        top_matches_professors.append([prof_key, prof_data['photo'], prof_data['url']])

    print("Top 5 Matched Professors:", top_matches_professors)
    return top_matches_professors



app = Flask(__name__)
CORS(app, resources={r'/api/*': {'origins': '*'}})

@app.route('/api/student', methods=['POST'])
def post_data():
    student_data = request.get_json()
    output = getSimilarity(student_data['researchInterests'] + student_data['paperTitles'])
    print(output)
    return output, 201 

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')