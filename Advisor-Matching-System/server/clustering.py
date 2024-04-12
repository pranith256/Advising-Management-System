import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import numpy as np

def load_data(filepath):
    with open(filepath, 'r') as file:
        return json.load(file)

def combine_interests_and_publications(data):
    combined = []
    for key, value in data.items():
        interests = " ".join(value["interests"])
        # publications = " ".join([pub["title"] + " " + pub["snippet"] for pub in value.get("publications", [])])
        combined.append(interests)
        # combined.append(interests + " " + publications)
    return combined

def get_top_features_cluster(tfidf_array, prediction, n_feats):
    labels = np.unique(prediction)
    dfs = []
    for label in labels:
        id_temp = np.where(prediction==label)  # Indices for each cluster
        x_means = np.mean(tfidf_array[id_temp], axis = 0)  # Mean tf-idf value for each term in the cluster
        sorted_means = np.argsort(x_means)[::-1][:n_feats]  # Indices of terms with highest means
        features = vectorizer.get_feature_names_out()
        best_features = [(features[i], x_means[i]) for i in sorted_means]
        dfs.append(best_features)
    return dfs

# Load and combine data
prof_data = load_data('project/Advisor-Matching-System/server/FinalProfessorsData.json')
prof_combined = combine_interests_and_publications(prof_data)

# Vectorize data
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(prof_combined)

# Perform clustering
n_clusters = 10
kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(X)
clusters = kmeans.labels_

# Identify important terms in each cluster
top_terms = get_top_features_cluster(X.toarray(), clusters, 10) 

# Group and print professors by cluster and their top terms
clustered_professors = {i: [] for i in range(n_clusters)}
for idx, cluster in enumerate(clusters):
    professor_name = list(prof_data.keys())[idx]
    clustered_professors[cluster].append(professor_name)

for cluster, professors in clustered_professors.items():
    print(f"Cluster {cluster}:")
    for prof in professors:
        print(f" - {prof}")
    print("Top Matched Research Interests/Topics in this Cluster:")
    for term, score in top_terms[cluster]:
        print(f"   - {term} (score: {score:.2f})")
    print()
