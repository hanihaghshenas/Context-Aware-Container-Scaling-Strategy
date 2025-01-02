from owlready2 import *

# Load the ontology
ontology = get_ontology("../ontology/container_scaling.owl").load()

# Query Ontology
def query_ontology():
    print("Querying Ontology:")
    for container in ontology.Container.instances():
        contexts = container.HasContext
        for context in contexts:
            actions = context.Triggers
            print(f"{container} is associated with context {context} triggering actions {[action.name for action in actions]}")

# Test Query
if __name__ == "__main__":
    query_ontology()
