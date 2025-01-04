from models.similarity_model import load_container_data, compute_similarity, find_clusters
from models.collaborative_model import create_user_item_matrix, apply_truncated_svd, predict_scaling_actions
from ontology.define_ontology import define_ontology  # Import ontology definition function
from ontology.query_ontology import query_ontology  # Import ontology query function
from owlready2 import get_ontology
import numpy as np

# Load the ontology dynamically after defining it
def update_and_load_ontology():
    define_ontology()  # Update the ontology dynamically
    return get_ontology("ontology/container_scaling.owl").load()

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
    ontology = update_and_load_ontology()  # Automatically update and load the ontology
    print("Ontology loaded successfully.")
    query_ontology()  # Optional query call to display all ontology data
    # Query and display contexts and actions for containers
    for container in ontology.Container.instances():
        print(f"Processing container: {container.name}")
        contexts = container.HasContext
        for context in contexts:
            actions = context.Triggers
            action_reasons = [action.name for action in actions]
            print(f"{container.name}: Context - {context.name}, Actions - {action_reasons}")

    # Step 5: Scaling Decisions Loop with Ontology
    print("\nScaling Decisions:")
    container_names = list(container_data_dict.keys())  # Use container_data_dict for consistent referencing
    for i in range(hybrid_scores.shape[0]):  # Loop over containers
        container_name = container_names[i]
        max_score = np.max(hybrid_scores[i])
        reasons = []

        if max_score > 0.7:  # Scaling threshold
            # Check contributions from CBF and CF scores
            if cbf_scores[i, np.argmax(hybrid_scores[i])] > 0.5:
                reasons.append("high similarity to containers with high resource usage (CBF)")
            if cf_scores[i, np.argmax(hybrid_scores[i])] > 0.5:
                reasons.append("historical workload patterns predicting increased demand (CF)")

            # Ontology-based reasoning
            container_instance = ontology.search_one(iri=f"*{container_name}")
            if container_instance:
                for context in container_instance.HasContext:
                    for action in context.Triggers:
                        reasons.append(f"contextual action '{action.name}' due to context '{context.name}'")

            # Combine reasons into a single explanation
            if reasons:
                reason_str = " and ".join(reasons)
                print(f"{container_name}: Scaling action required due to {reason_str}")
            else:
                print(f"{container_name}: Scaling action required but no specific reasons identified.")
        else:
            print(f"{container_name}: No scaling action required (max score: {max_score:.2f}).")


# Test Hybrid Model
if __name__ == "__main__":
    from simulation.trigger_workloads import workloads  # Import workloads from simulation
    hybrid_model_with_ontology(workloads)
