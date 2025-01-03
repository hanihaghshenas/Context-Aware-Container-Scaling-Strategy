from .simulate_workload import generate_workload, load_container_data

def trigger_workloads():
    # Load container data
    container_data = load_container_data()

    # Collect simulated workloads
    workloads = []
    for container_id, container_name in enumerate(container_data.keys(), start=1):
        result = generate_workload.delay(container_id, container_name)  # Send task to worker
        workload = result.get(timeout=10)  # Wait for result
        print(workload)
        workloads.append((container_name, workload))

    return workloads
