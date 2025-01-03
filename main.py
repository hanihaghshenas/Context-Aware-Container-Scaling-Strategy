import json
from models.hybrid_model import hybrid_model_with_ontology
from simulation.trigger_workloads import trigger_workloads
import random

# Generate container data without workloads
def generate_container_data(num_containers=5):
    container_data = {}
    for i in range(num_containers):
        container_data[f"Container{i+1}"] = {
            "CPU": random.randint(10, 100),
            "Memory": random.randint(50, 500),
            "Network": random.randint(5, 50),
        }
    return container_data

# Merge workloads into container data
def merge_workloads_with_container_data(container_data, workloads):
    for container_name, workload_str in workloads:
        workload_value = int(workload_str.split()[-1][:-1])  # Extract workload percentage
        if container_name in container_data:
            container_data[container_name]["Workload"] = workload_value
    return container_data

# Save data to a file
def save_to_file(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

# Main entry point
if __name__ == "__main__":
    print("Starting the Context-Aware Container Scaling Project...")

    # Step 1: Generate and save container metadata
    print("Generating container metadata...")
    container_data = generate_container_data(num_containers=5)
    save_to_file(container_data, "data/container_data.json")
    print(f"Container metadata saved to 'data/container_data.json'")

    # Step 2: Generate workloads dynamically for containers
    print("Generating workloads for containers...")
    workloads = trigger_workloads()  # Trigger workload generation
    print("Generated workloads:", workloads)

    # Step 3: Merge workloads with container metadata
    print("Merging workloads with container data...")
    container_data = merge_workloads_with_container_data(container_data, workloads)
    save_to_file(container_data, "data/container_data.json")
    print(f"Updated container data saved to 'data/container_data.json'")

    # Step 4: Trigger the hybrid recommender system
    print("Starting the Hybrid Recommender System...")
    hybrid_model_with_ontology(workloads)
