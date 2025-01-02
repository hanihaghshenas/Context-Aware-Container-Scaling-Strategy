from owlready2 import *

# Create a new ontology
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

    class ScaleUp(ScalingAction): pass
    class ScaleDown(ScalingAction): pass

    # Define Relationships
    class HasContext(Container >> Context): pass
    class Triggers(Context >> ScalingAction): pass

    # Add Instances for Containers
    container1 = CPUHeavy("Container1")
    container2 = MemoryHeavy("Container2")
    container3 = CPUHeavy("Container3")
    container4 = MemoryHeavy("Container4")

    # Add Instances for Contexts and Scaling Actions
    peak_hours_instance = PeakHours("peak_hours_instance")
    region_europe_instance = GeographicRegion("region_europe_instance")
    region_america_instance = GeographicRegion("region_america_instance")

    scale_up_instance = ScaleUp("scale_up_instance")
    scale_down_instance = ScaleDown("scale_down_instance")

    # Link containers to contexts
    container1.HasContext.append(peak_hours_instance)
    container2.HasContext.append(region_europe_instance)
    container3.HasContext.append(region_america_instance)
    container4.HasContext.append(peak_hours_instance)

    # Link contexts to scaling actions
    peak_hours_instance.Triggers.append(scale_up_instance)
    region_europe_instance.Triggers.append(scale_down_instance)
    region_america_instance.Triggers.append(scale_up_instance)

# Save Ontology
ontology.save(file="ontology/container_scaling.owl")
print("Ontology saved as 'container_scaling.owl'")
