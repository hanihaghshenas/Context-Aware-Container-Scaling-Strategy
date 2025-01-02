from sklearn.decomposition import TruncatedSVD
import pandas as pd
import numpy as np

# User-Item Matrix with Actual Workloads
def create_user_item_matrix(workloads):
    # Convert workloads into a workload-container matrix
    data = pd.DataFrame({
        'Container1': [workloads[0], 0, 0],
        'Container2': [0, workloads[1], 0],
        'Container3': [0, 0, workloads[2]],
        'Container4': [workloads[3], 0, 0]
    }, index=['Workload1', 'Workload2', 'Workload3'])
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
def collaborative_filtering(workloads):
    # Step 1: Create User-Item Matrix
    user_item_matrix = create_user_item_matrix(workloads)

    # Step 2: Apply Truncated SVD
    svd, latent_features = apply_truncated_svd(user_item_matrix)

    # Step 3: Reconstruct and Predict
    predict_scaling_actions(svd, user_item_matrix)

# Test CF
if __name__ == "__main__":
    # Example workloads; replace with actual workloads from simulation
    simulated_workloads = [63, 74, 84, 56]
    collaborative_filtering(simulated_workloads)
