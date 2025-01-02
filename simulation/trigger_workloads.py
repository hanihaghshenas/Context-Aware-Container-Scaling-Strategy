from .simulate_workload import generate_workload

# Trigger workload generation for containers
for container_id in range(1, 5):  # Simulating 4 containers
    result = generate_workload.delay(container_id)  # Send task to the worker
    print(result.get(timeout=10))  # Wait for and display the result
