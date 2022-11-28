# Wing Parametric Description (values in SI)
WING = {
    "span": 43.58, # meter
    "root_chord": 6.86, # meter
    "taper_ratio": 0.27
} 

def distribute_stringers(fspar, rspar, nstringers):
    stringers = []
    if nstringers == 0: return stringers
    dist = (rspar - fspar) / nstringers
    for i in range(nstringers):
        stringers.append(fspar + (i+(1/2))*dist)
    return stringers

# Parametric Description of Wingbox
WINGBOX = {
    "front_spar": 0.2,
    "rear_spar": 0.65,
    "other_spars": [(0.3,0.4),(0.4,0.7)], # (x/c position value, y/(b/2) value of end of spar)
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

G = 9.80665

# Critical Load Parameters (in SI)
CRIT = {
    "load_factor": 3.75,
    "distributed_loads": [(-199.8707 * G, 4355.183221 * G)], # Wing Mass
    "point_loads": [(7277 * G, 8.374)], # Engine Mass
    "cld": 0.9,
    "dynp": 4838.801824
}
