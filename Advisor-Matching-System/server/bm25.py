import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
from rank_bm25 import BM25Okapi
import numpy as np

def load_data(filepath):
    with open(filepath, 'r') as file:
        return json.load(file)

def combine_interests_and_publications(data):
    combined = []
    for key, value in data.items():
        interests = " ".join(value["interests"])
        publications = " ".join([pub["title"] + " " + pub["snippet"] for pub in value.get("publications", [])])
        combined.append(interests + " " + publications)
    return combined

def vectorize_with_bm25(texts):
    tokenized_texts = [doc.split(" ") for doc in texts]
    bm25 = BM25Okapi(tokenized_texts)
    return bm25

def calculate_similarity(bm25, query):
    query_tokens = query.split(" ")
    scores = bm25.get_scores(query_tokens)
    return scores


# Load data
prof_data = load_data('FinalProfessorsData.json')

# Combine interests and publications
prof_combined = combine_interests_and_publications(prof_data)

# Vectorize with BM25
bm25 = vectorize_with_bm25(prof_combined)

student_query = "computer vision deep learning"

# Calculate similarity
similarities = calculate_similarity(bm25, student_query)

# Find top matches
top_matches_indices = np.argsort(similarities)[-5:][::-1]
top_matches_professors = [list(prof_data.keys())[i] for i in top_matches_indices]

print("Top 5 Matched Professors:", top_matches_professors)
