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
    peak_hours = PeakHours("PeakHours")
    region_europe = GeographicRegion("RegionEurope")
    region_america = GeographicRegion("RegionAmerica")

    scale_up = ScaleUp("ScaleUp")
    scale_down = ScaleDown("ScaleDown")

    # Link containers to contexts
    container1.HasContext.append(peak_hours)
    container2.HasContext.append(region_europe)
    container3.HasContext.append(region_america)
    container4.HasContext.append(peak_hours)

    # Link contexts to scaling actions
    peak_hours.Triggers.append(scale_up)
    region_europe.Triggers.append(scale_down)
    region_america.Triggers.append(scale_up)

# Save Ontology
ontology.save(file="ontology/container_scaling.owl")
print("Ontology saved as 'container_scaling.owl'")
