import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Load the combined data from the previously saved JSON file
with open('project/Advisor-Matching-System/server/FinalProfessorsData.json', 'r') as file:
    combined_data = json.load(file)

student_interests = ["computer vision deep learning Using Deep Learning and Augmented Reality to Improve Accessibility: Inclusive Conversations Using Diarization, Captions, and Visualization"]

student_interests_str = " ".join(student_interests)

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
top_matches_professors = [professor_names[i] for i in top_matches_indices]

print("Top 5 Matched Professors:", top_matches_professors)
