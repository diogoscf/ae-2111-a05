# Wing Parametric Description (values in SI)
WING = {
    "span": 43.58, # meter
    "root_chord": 6.86, # meter
    "taper_ratio": 0.27
}

# Parametric Description of Wingbox
WINGBOX = {
    "front_spar": 0.2,
    "rear_spar": 0.65,
    "other_spars": [(0.3,0.4),(0.5,0.7)], # (x/c position value, y/(b/2) value of end of spar)
    "spar_thickness": 8E-3, # meter
    "skin_thickness": 8E-3, # meter
    "stringer_area": 60E-6, # square meter
    "stringers_top": [0.25,0.3,0.4,0.5, 0.6],
    "stringers_bottom": [0.25,0.3,0.4,0.5,0.6]
}

# Wingbox Material Parameters (in SI)
MAT = {
    "E": 68.9E9, # pascal
    "G": 26E9  # pascal
}

# Critical Load Parameters (in SI)
CRIT = {
    "load_factor": 3.75,
    "point_loads": [],
    "cld": 1
}