from sklearn.decomposition import TruncatedSVD
import pandas as pd
import numpy as np
import json

# Load container data from JSON
def load_container_data(filename="data/container_data.json"):
    with open(filename, "r") as f:
        return json.load(f)

# Create User-Item Matrix from Workloads
def create_user_item_matrix(container_data):
    if isinstance(container_data, pd.DataFrame):
        # Convert DataFrame to dictionary format
        container_data = container_data.set_index("Container").to_dict("index")

    # Ensure container_data is a dictionary
    workloads = [data["Workload"] for data in container_data.values()]
    num_containers = len(container_data)
    data = pd.DataFrame(
        np.eye(num_containers) * workloads,  # Create diagonal workload matrix
        columns=container_data.keys(),
        index=[f"Workload{i + 1}" for i in range(num_containers)],
    )
    print("\n=== User-Item Matrix ===")
    print(data)
    return data


# Apply Truncated SVD
def apply_truncated_svd(user_item_matrix, n_components=2):
    svd = TruncatedSVD(n_components=n_components)
    latent_features = svd.fit_transform(user_item_matrix)
    print("\n=== Latent Features (Reduced Dimensions) ===")
    print(latent_features)
    return svd, latent_features

# Make Predictions
def predict_scaling_actions(svd, user_item_matrix):
    reconstructed_matrix = svd.inverse_transform(svd.transform(user_item_matrix))
    print("\n=== Reconstructed Matrix (Predictions) ===")
    print(np.round(reconstructed_matrix, 2))  # Rounded for readability
    return reconstructed_matrix

# Main Function for Collaborative Filtering
def collaborative_filtering():
    # Step 1: Load container data
    container_data = load_container_data()

    # Step 2: Create User-Item Matrix
    user_item_matrix = create_user_item_matrix(container_data)

    # Step 3: Apply Truncated SVD
    svd, latent_features = apply_truncated_svd(user_item_matrix)

    # Step 4: Reconstruct and Predict
    predict_scaling_actions(svd, user_item_matrix)

# Test CF
if __name__ == "__main__":
    # Example workloads; replace with actual workloads from simulation
    simulated_workloads = [63, 74, 84, 56]
    collaborative_filtering()
