from sklearn.decomposition import TruncatedSVD
import pandas as pd
import numpy as np

# User-Item Matrix: Workload-Container Scaling Actions
def create_user_item_matrix():
    # Example data
    data = pd.DataFrame({
        'Container1': [1, 0, 1],
        'Container2': [0, 1, 1],
        'Container3': [1, 0, 0],
        'Container4': [0, 1, 0]
    }, index=['Workload1', 'Workload2', 'Workload3'])
    return data

# Apply Truncated SVD
def apply_truncated_svd(user_item_matrix, n_components=2):
    svd = TruncatedSVD(n_components=n_components)
    latent_features = svd.fit_transform(user_item_matrix)
    return svd, latent_features

# Make Predictions
def predict_scaling_actions(svd, user_item_matrix):
    reconstructed_matrix = svd.inverse_transform(svd.transform(user_item_matrix))
    return reconstructed_matrix

# Main Function for Collaborative Filtering
def collaborative_filtering():
    # Step 1: Create User-Item Matrix
    user_item_matrix = create_user_item_matrix()
    print("\nUser-Item Matrix:")
    print(user_item_matrix)

    # Step 2: Apply Truncated SVD
    svd, latent_features = apply_truncated_svd(user_item_matrix)
    print("\nLatent Features (Reduced Dimensions):")
    print(latent_features)

    # Step 3: Reconstruct and Predict
    reconstructed_matrix = predict_scaling_actions(svd, user_item_matrix)
    print("\nReconstructed Matrix (Predictions):")
    print(np.round(reconstructed_matrix, 2))  # Rounded for readability

# Test CF
if __name__ == "__main__":
    collaborative_filtering()
