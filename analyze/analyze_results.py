import json
import matplotlib.pyplot as plt
from collections import Counter
import os

# Load results from JSON file
def load_results(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

# Analyze trends from results
def analyze_results(results):
    scaling_counts = Counter()
    contextual_reasons = Counter()

    for entry in results:
        decisions = entry.get("scaling_decisions", [])
        for decision in decisions:
            scaling_counts[decision["action"]] += 1
            for reason in decision.get("reasons", []):
                contextual_reasons[reason] += 1

    return scaling_counts, contextual_reasons

# Generate visualizations
def generate_visualizations(scaling_counts, contextual_reasons):
    # Bar chart for scaling actions
    plt.figure(figsize=(10, 6))
    actions, counts = zip(*scaling_counts.items())
    plt.bar(actions, counts, color='skyblue')
    plt.title("Scaling Action Frequencies")
    plt.xlabel("Scaling Action")
    plt.ylabel("Frequency")
    plt.show()

    # Bar chart for contextual reasons
    plt.figure(figsize=(12, 8))
    reasons, frequencies = zip(*contextual_reasons.most_common(10))
    plt.barh(reasons, frequencies, color='lightcoral')
    plt.title("Top 10 Contextual Reasons for Scaling Decisions")
    plt.xlabel("Frequency")
    plt.ylabel("Contextual Reasons")
    plt.gca().invert_yaxis()
    plt.show()

if __name__ == "__main__":
    # Step 1: Load results

    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, '../data/results.json')
    results = load_results(file_path)

    # Step 2: Analyze results
    scaling_counts, contextual_reasons = analyze_results(results)

    # Step 3: Generate visualizations
    generate_visualizations(scaling_counts, contextual_reasons)
