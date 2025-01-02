from models.similarity_model import load_container_data, compute_similarity, find_clusters
from models.collaborative_model import create_user_item_matrix, apply_truncated_svd, predict_scaling_actions
from ontology.query_ontology import query_ontology  # Import ontology query function
from owlready2 import get_ontology
import numpy as np

# Load the ontology
ontology = get_ontology("../ontology/container_scaling.owl").load()

# Hybrid Model with Ontology Integration
def hybrid_model_with_ontology():
    # Step 1: Content-Based Filtering (CBF)
    print("=== Content-Based Filtering ===")
    container_data = load_container_data()  # Load unified container data
    similarity_matrix = compute_similarity(container_data)
    clusters = find_clusters(similarity_matrix, container_data['Container'])
    print("\nClusters (CBF):")
    for container, group in clusters.items():
        print(f"{container} is similar to: {group}")

    # Step 2: Collaborative Filtering (CF)
    print("\n=== Collaborative Filtering ===")
    user_item_matrix = create_user_item_matrix()  # Load unified user-item matrix
    svd, latent_features = apply_truncated_svd(user_item_matrix)
    reconstructed_matrix = predict_scaling_actions(svd, user_item_matrix)
    print("\nReconstructed Matrix (CF Predictions):")
    print(np.round(reconstructed_matrix, 2))

    # Step 3: Combine CBF and CF Scores
    print("\n=== Hybrid Model ===")
    # Normalize similarity_matrix and reconstructed_matrix to the same scale
    cbf_scores = similarity_matrix[:reconstructed_matrix.shape[0], :reconstructed_matrix.shape[1]]
    cbf_scores = cbf_scores / np.max(cbf_scores)  # Normalize to [0, 1]
    cf_scores = reconstructed_matrix / np.max(reconstructed_matrix)  # Normalize to [0, 1]

    # Weighted combination of CBF and CF scores
    alpha = 0.6  # Weight for CBF
    beta = 0.4   # Weight for CF
    hybrid_scores = alpha * cbf_scores + beta * cf_scores

    print("Hybrid Scores (CBF + CF):")
    print(np.round(hybrid_scores, 2))

    # Step 4: Ontology-Based Contextual Reasoning
    print("\n=== Ontology Integration ===")
    for container in ontology.Container.instances():
        contexts = container.HasContext
        for context in contexts:
            actions = context.Triggers
            action_reasons = [action.name for action in actions]
            print(f"{container.name}: Context - {context.name}, Actions - {action_reasons}")

    # Step 5: Scaling Decisions Loop with Ontology
    print("\nScaling Decisions:")
    for i in range(hybrid_scores.shape[0]):  # Loop over available rows in hybrid_scores
        max_score = np.max(hybrid_scores[i])
        max_index = np.argmax(hybrid_scores[i])  # Index of the highest hybrid score
        reasons = []

        if max_score > 0.7:  # Scaling threshold
            # Check contributions from CBF and CF scores
            if cbf_scores[i, max_index] > 0.5:
                reasons.append("high similarity to containers with high resource usage")
            if cf_scores[i, max_index] > 0.5:
                reasons.append("historical workload patterns predicting increased demand")

            # Query ontology for additional context-based recommendations
            container_instance = ontology.search_one(iri=f"*{container_data['Container'][i]}")
            if container_instance:
                for context in container_instance.HasContext:
                    for action in context.Triggers:
                        reasons.append(f"contextual action '{action.name}' due to '{context.name}'")

            # Combine reasons into a single explanation
            reason_str = " and ".join(reasons)
            print(f"{container_data['Container'][i]}: Scaling action required due to {reason_str}")


# Test Hybrid Model
if __name__ == "__main__":
    hybrid_model_with_ontology()
