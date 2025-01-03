from celery import Celery
import json
import time
import random

app = Celery(
    'simulation',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'  # Enable result backend
)

# Load container data from JSON
def load_container_data(filename="data/container_data.json"):
    with open(filename, 'r') as f:
        container_data = json.load(f)
    return container_data

@app.task
def generate_workload(container_id, container_name):
    workload = random.randint(50, 100)  # Random CPU usage
    time.sleep(random.uniform(0.1, 0.5))  # Simulate processing time
    return f"{container_name}: Workload {workload}%"
