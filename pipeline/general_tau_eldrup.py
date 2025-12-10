import numpy as np
import tau_eldrup

def determine_radii():
    lifetime_ns = np.linspace(1E-6, 20, 1000)
    diameter = tau_eldrup.tau_to_fvd(lifetime_ns)
    return lifetime_ns, diameter

lt, d = determine_radii()

for i, l in enumerate(lt):
    print(f"{l:.6f},{d[i]:.6f}")