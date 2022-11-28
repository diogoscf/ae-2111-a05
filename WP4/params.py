# Wing Parametric Description (values in SI)
WING = {
    "span": 43.58, # meter
    "root_chord": 6.86, # meter
    "taper_ratio": 0.27
} 

def distribute_stringers(fspar, rspar, nstringers):
    stringers = []
    for i in range(nstringers):
        stringers.append(fspar + (i+1)*((rspar - fspar) / (nstringers + 1)))
    return stringers

# Parametric Description of Wingbox
WINGBOX = {
    "front_spar": 0.2,
    "rear_spar": 0.65,
    "other_spars": [(0.3,0.4),(0.5,0.7)], # (x/c position value, y/(b/2) value of end of spar)
    "spar_thickness": 8E-3, # meter
    "skin_thickness": 5E-3, # meter
    "stringer_area": 60E-6, # square meter
    "stringers_top": distribute_stringers(0.2, 0.65, 8),
    "stringers_bottom": distribute_stringers(0.2, 0.65, 8)
}

# Wingbox Material Parameters (in SI)
MAT = {
    "E": 68.9E9, # pascal
    "G": 26E9 # pascal
} 

# Critical Load Parameters (in SI)
CRIT = {
    "load_factor": 3.75,
    "point_loads": [],
    "cld": 0.9
}
