from .simulate_workload import generate_workload

# Collect simulated workloads
workloads = []

# Trigger workload generation for containers
for container_id in range(1, 5):  # Simulating 4 containers
    result = generate_workload.delay(container_id)  # Send task to worker
    workload = result.get(timeout=10)  # Wait for result
    print(workload)
    workloads.append((container_id, workload))

# Save workloads to pass to hybrid model
print("\nCollected Workloads:")
for container_id, workload in workloads:
    print(f"Container {container_id}: {workload}")
