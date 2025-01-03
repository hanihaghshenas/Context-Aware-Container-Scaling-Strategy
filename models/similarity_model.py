import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import json

# 1. Load Container Metrics from JSON
def load_container_data(filename="data/container_data.json"):
    with open(filename, "r") as f:
        container_data = json.load(f)

    # Convert to DataFrame
    data = pd.DataFrame.from_dict(container_data, orient="index").reset_index()
    data.rename(columns={"index": "Container"}, inplace=True)
    print("=== Loaded Data ===")
    print(data)
    return data

# 2. Compute Cosine Similarity
def compute_similarity(data):
    features = data.drop("Container", axis=1)
    similarity_matrix = cosine_similarity(features)
    print("\n=== Cosine Similarity Matrix ===")
    print(similarity_matrix)
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
    print("\n=== Clusters Based on Similarity ===")
    for container, similar in clusters.items():
        print(f"{container} is similar to: {similar}")
    return clusters

# 4. Scaling Decision Logic
def scale_containers(container, clusters, current_usage, usage_threshold=80):
    if current_usage[container] > usage_threshold:
        print(f"Scaling up cluster for container {container}")
        for similar_container in clusters[container]:
            print(f"Allocating resources to {similar_container} (similar to {container})")
    else:
        print(f"No scaling required for container {container}")


# Main Function (optional for testing as a standalone script)
def main(workloads):
    # Step 1: Load Data
    data = load_container_data(workloads)
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
    # Example workloads; replace with actual workloads from simulation
    simulated_workloads = [63, 74, 84, 56]
    main(simulated_workloads)
