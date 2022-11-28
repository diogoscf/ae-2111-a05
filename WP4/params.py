# Wing Parametric Description (values in SI)
WING = {"span": 43.58, "root_chord": 6.86, "taper_ratio": 0.27}  # meter  # meter

# Parametric Description of Wingbox
WINGBOX = {
    "front_spar": 0.2,
    "rear_spar": 0.65,
    "other_spars": [
        (0.3, 0.4),
        (0.5, 0.7),
    ],  # (x/c position value, y/(b/2) value of end of spar)
    "spar_thickness": 0.02,  # meter
    "skin_thickness": 0.01,  # meter
    "stringer_area": 0.003,  # square meter
    "stringers_top": [0.2, 0.3, 0.4, 0.5],
    "stringers_bottom": [0.2, 0.3, 0.4, 0.5],
}

# Wingbox Material Parameters (in SI)
MAT = {"E": 68.9e9, "G": 26e9}  # pascal  # pascal

# Critical Load Parameters (in SI)
CRIT = {"load_factor": 1, "point_loads": [], "cld": 1}

# Universal constants (in SI)
UNIV = {"g": 9.80665}  # m/s^2
