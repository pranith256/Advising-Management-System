from flask import Flask, jsonify, request
from flask_cors import CORS
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def getSimilarity(student_interests):
    with open('FinalProfessorsData.json', 'r') as file:
        combined_data = json.load(file)

    # Combine the student's interests into a single string
    student_interests_str = student_interests
    print("Student Interests: ", student_interests_str)

    # Create a list of professor names and their combined interests
    professor_names = list(combined_data.keys())
    professor_interests = [" ".join(combined_data[prof]["interests"]) for prof in professor_names]

    # Combine student interests with professor interests
    all_interests = [student_interests_str] + professor_interests

    # Use TF-IDF to vectorize the interests
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(all_interests)

    # Calculate cosine similarity between the student and each professor
    student_vector = tfidf_matrix[0]
    professor_vectors = tfidf_matrix[1:]

    similarities = cosine_similarity(student_vector, professor_vectors).flatten()

    # Find the top 5 professors with the highest similarity
    top_matches_indices = similarities.argsort()[-5:][::-1]

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
    output = getSimilarity(student_data['researchInterests'])
    print(output)
    return output, 201 

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')