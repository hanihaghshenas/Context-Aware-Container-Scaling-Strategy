import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


# 1. Load Container Metrics
def load_container_data():
    # Example dataset
    data = pd.DataFrame({
        'Container': ['Container1', 'Container2', 'Container3', 'Container4'],
        'CPU': [30, 35, 80, 25],
        'Memory': [100, 95, 300, 120],
        'Network': [10, 12, 30, 9]
    })
    return data


# 2. Compute Cosine Similarity
def compute_similarity(data):
    features = data.drop('Container', axis=1)
    similarity_matrix = cosine_similarity(features)
    return similarity_matrix


# 3. Identify Clusters Based on Similarity
def find_clusters(similarity_matrix, containers, threshold=0.8):
    clusters = {}
    for i, container in enumerate(containers):
        clusters[container] = [
            containers[j]
            for j in range(len(similarity_matrix))
            if similarity_matrix[i, j] >= threshold and i != j
        ]
    return clusters


# 4. Scaling Decision Logic
def scale_containers(container, clusters, current_usage, usage_threshold=80):
    if current_usage[container] > usage_threshold:
        print(f"Scaling up cluster for container {container}")
        for similar_container in clusters[container]:
            print(f"Allocating resources to {similar_container} (similar to {container})")
    else:
        print(f"No scaling required for container {container}")


# Main Function to Run the Workflow
def main():
    # Step 1: Load Data
    data = load_container_data()
    print("Container Metrics:\n", data)

    # Step 2: Compute Similarity
    similarity_matrix = compute_similarity(data)
    print("\nCosine Similarity Matrix:\n", similarity_matrix)

    # Step 3: Find Clusters
    clusters = find_clusters(similarity_matrix, data['Container'])
    print("\nClusters:")
    for container, group in clusters.items():
        print(f"{container} is similar to: {group}")

    # Step 4: Example Scaling Decisions
    current_usage = {'A': 85, 'B': 90, 'C': 70, 'D': 50}
    scale_containers('A', clusters, current_usage)


if __name__ == "__main__":
    main()
