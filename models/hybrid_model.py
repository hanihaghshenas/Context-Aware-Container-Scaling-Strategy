from models.similarity_model import load_container_data, compute_similarity, find_clusters
from models.collaborative_model import create_user_item_matrix, apply_truncated_svd, predict_scaling_actions
from ontology.query_ontology import query_ontology
from owlready2 import get_ontology
import numpy as np

# Load the ontology
ontology = get_ontology("ontology/container_scaling.owl").load()

# Hybrid Model with Ontology Integration
def hybrid_model_with_ontology(workloads):
    print("=== Simulated Workloads ===")
    for container_id, workload in workloads:
        print(f"Container {container_id}: {workload}")

    # Parse workloads into numerical values
    actual_workloads = [int(workload.split()[-1][:-1]) for _, workload in workloads]
    print("\nParsed Workloads:", actual_workloads)

    # Step 1: Content-Based Filtering (CBF)
    print("\n=== Content-Based Filtering ===")
    container_data = load_container_data()  # Load data from JSON
    similarity_matrix = compute_similarity(container_data)
    clusters = find_clusters(similarity_matrix, container_data['Container'])
    print("\nClusters (CBF):")
    for container, group in clusters.items():
        print(f"{container} is similar to: {group}")

    # Step 2: Collaborative Filtering (CF)
    print("\n=== Collaborative Filtering ===")
    # Load container data
    container_data = load_container_data()
    # Create the user-item matrix using container workloads
    user_item_matrix = create_user_item_matrix(container_data)
    svd, latent_features = apply_truncated_svd(user_item_matrix)
    reconstructed_matrix = predict_scaling_actions(svd, user_item_matrix)
    print("\nReconstructed Matrix (CF Predictions):")
    print(np.round(reconstructed_matrix, 2))

    # Step 3: Combine CBF and CF Scores
    print("\n=== Hybrid Model ===")

    # Align dimensions between CBF and CF scores
    cbf_scores = similarity_matrix[:reconstructed_matrix.shape[0], :reconstructed_matrix.shape[1]]
    cbf_scores = cbf_scores / np.max(cbf_scores)  # Normalize to [0, 1]
    cf_scores = reconstructed_matrix / np.max(reconstructed_matrix)  # Normalize to [0, 1]

    # Convert container data to dictionary for consistency
    container_data_dict = container_data.set_index("Container").to_dict("index")

    # Ensure workload_scores matches the number of rows in cbf_scores
    workload_scores = np.array([data["Workload"] for data in container_data_dict.values()])[:cbf_scores.shape[0]] / 100

    # Combine scores with weights
    alpha, beta, gamma = 0.5, 0.3, 0.2  # Weights for CBF, CF, and workload contributions
    hybrid_scores = alpha * cbf_scores + beta * cf_scores + gamma * workload_scores[:, None]

    # Display the Hybrid Scores
    print("Hybrid Scores (CBF + CF + Workloads):")
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
        reasons = []

        if max_score > 0.7:  # Scaling threshold
            # Contributions from CBF and CF scores
            if cbf_scores[i, np.argmax(hybrid_scores[i])] > 0.5:
                reasons.append("high similarity to containers with high resource usage")
            if cf_scores[i, np.argmax(hybrid_scores[i])] > 0.5:
                reasons.append("historical workload patterns predicting increased demand")

            # Ontology-based reasoning
            container_instance = ontology.search_one(iri=f"*{list(container_data.keys())[i]}")
            if container_instance:
                for context in container_instance.HasContext:
                    for action in context.Triggers:
                        reasons.append(f"contextual action '{action.name}' due to '{context.name}'")

            reason_str = " and ".join(reasons)
            print(f"{list(container_data.keys())[i]}: Scaling action required due to {reason_str}")


# Test Hybrid Model
if __name__ == "__main__":
    from simulation.trigger_workloads import workloads  # Import workloads from simulation
    hybrid_model_with_ontology(workloads)
