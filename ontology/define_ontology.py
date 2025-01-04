from owlready2 import *
import json

# Load container data from JSON
def load_container_data(filename="data/container_data.json"):
    with open(filename, "r") as f:
        return json.load(f)

# Define and save the ontology
def define_ontology():
    # Create or update the ontology
    ontology = get_ontology("http://example.org/container_scaling.owl")
    with ontology:
        # Define Classes
        class Container(Thing): pass
        class Context(Thing): pass
        class ScalingAction(Thing): pass

        # Define Subclasses
        class CPUHeavy(Container): pass
        class MemoryHeavy(Container): pass

        class PeakHours(Context): pass
        class GeographicRegion(Context): pass
        class HighNetworkUsage(Context): pass
        class LowMemoryAvailability(Context): pass

        class ScaleUp(ScalingAction): pass
        class ScaleDown(ScalingAction): pass
        class NoAction(ScalingAction): pass

        # Define Relationships
        class HasContext(Container >> Context): pass
        class Triggers(Context >> ScalingAction): pass

        # Add Instances for Contexts and Scaling Actions
        peak_hours_instance = PeakHours("peak_hours_instance")
        region_europe_instance = GeographicRegion("region_europe_instance")
        region_america_instance = GeographicRegion("region_america_instance")
        high_network_instance = HighNetworkUsage("high_network_instance")
        low_memory_instance = LowMemoryAvailability("low_memory_instance")

        scale_up_instance = ScaleUp("scale_up_instance")
        scale_down_instance = ScaleDown("scale_down_instance")
        no_action_instance = NoAction("no_action_instance")

        # Link contexts to scaling actions
        peak_hours_instance.Triggers.append(scale_up_instance)
        region_europe_instance.Triggers.append(scale_down_instance)
        region_america_instance.Triggers.append(scale_up_instance)
        high_network_instance.Triggers.append(scale_up_instance)
        low_memory_instance.Triggers.append(scale_down_instance)

        # Dynamically Add Instances for Containers
        container_data = load_container_data()

        for container_name, data in container_data.items():
            # Define container type based on CPU and memory
            if data["CPU"] > 70:
                container_instance = CPUHeavy(container_name)
            else:
                container_instance = MemoryHeavy(container_name)

            # Assign contexts based on workload and usage patterns
            if data["Workload"] > 80:
                container_instance.HasContext.append(peak_hours_instance)

            if data["Memory"] < 150:
                container_instance.HasContext.append(low_memory_instance)

            if data["Network"] > 30:
                container_instance.HasContext.append(high_network_instance)

            # Geographic context (e.g., based on container name as a placeholder)
            if "1" in container_name or "3" in container_name:
                container_instance.HasContext.append(region_america_instance)
            else:
                container_instance.HasContext.append(region_europe_instance)

            # Ensure that all containers have at least one context
            if not container_instance.HasContext:
                container_instance.HasContext.append(no_action_instance)

            # Save the ontology
            ontology.save(file="ontology/container_scaling.owl")
            print("Ontology dynamically updated and saved.")

if __name__ == "__main__":
    define_ontology()