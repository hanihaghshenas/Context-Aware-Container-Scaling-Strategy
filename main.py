import json
from models.hybrid_model import hybrid_model_with_ontology
from simulation.trigger_workloads import trigger_workloads
import random
import os

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

# Load or initialize a file
def load_or_initialize_file(filename, default_content):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            try:
                content = f.read().strip()  # Read and strip whitespace
                if not content:  # Check if the file is empty
                    raise ValueError("File is empty")
                return json.loads(content)
            except (json.JSONDecodeError, ValueError):
                # If file is empty or invalid JSON, initialize it with default content
                with open(filename, 'w') as fw:
                    json.dump(default_content, fw, indent=4)
                return default_content
    else:
        # If the file doesn't exist, create it with default content
        with open(filename, 'w') as f:
            json.dump(default_content, f, indent=4)
        return default_content


# Save data to a file
def save_to_file(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

# Summarize scaling results for JSON
def summarize_scaling_decisions(scaling_decisions):
    summary = {
        "total_containers": len(scaling_decisions),
        "scale_up": sum(1 for d in scaling_decisions if d["action"] == "Scaling required"),
        "no_action": sum(1 for d in scaling_decisions if d["action"] == "No scaling"),
        "common_reasons": {}
    }

    # Aggregate reasons across decisions
    reason_counts = {}
    for decision in scaling_decisions:
        for reason in decision["reasons"]:
            if reason not in reason_counts:
                reason_counts[reason] = 0
            reason_counts[reason] += 1

    # Get top common reasons
    summary["common_reasons"] = {
        reason: count for reason, count in sorted(reason_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    }
    return summary

# Main entry point
if __name__ == "__main__":
    print("Starting the Context-Aware Container Scaling Project...")

    # File paths
    container_file = "data/container_data.json"
    workload_file = "data/workload_data.json"
    results_file = "data/results.json"

    # Step 1: Generate and save container metadata
    print("Generating container metadata...")
    container_data = generate_container_data(num_containers=5)
    save_to_file(container_data, container_file)
    print(f"Container metadata saved to '{container_file}'")

    # Step 2: Generate workloads dynamically for containers
    print("Generating workloads for containers...")
    workloads = trigger_workloads()  # Trigger workload generation
    print("Generated workloads:", workloads)

    # Step 3: Save workloads to cumulative workload data
    workload_data = load_or_initialize_file(workload_file, [])
    workload_data.append(workloads)  # Append current workloads
    save_to_file(workload_data, workload_file)
    print(f"Workloads saved to '{workload_file}'")

    # Step 4: Merge workloads with container metadata
    print("Merging workloads with container data...")
    container_data = merge_workloads_with_container_data(container_data, workloads)
    save_to_file(container_data, container_file)
    print(f"Updated container data saved to '{container_file}'")

    # Step 5: Trigger the hybrid recommender system
    print("Starting the Hybrid Recommender System...")
    hybrid_scores, scaling_decisions = hybrid_model_with_ontology(workloads)

    # Step 6: Save results to results file
    print("Saving results...")
    results = load_or_initialize_file(results_file, [])
    results.append({
        "workloads": workloads,
        "hybrid_scores": hybrid_scores.tolist(),  # Save NumPy array as list
        "scaling_decisions": scaling_decisions,
        "summary": summarize_scaling_decisions(scaling_decisions)  # Add summary
    })
    save_to_file(results, results_file)
    print(f"Results saved to '{results_file}'")
