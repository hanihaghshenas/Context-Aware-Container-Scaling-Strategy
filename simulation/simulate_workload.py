from celery import Celery
import random
import time

app = Celery('simulation', broker='redis://localhost:6379/0')

@app.task
def generate_workload(container_id):
    workload = random.randint(50, 100)  # Random CPU usage
    time.sleep(random.uniform(0.1, 0.5))  # Simulate processing time
    return f"Container {container_id}: Workload {workload}%"
