from design_options import *

# Wing Parametric Description (values in SI)
WING = {
    "span": 43.58,  # meter
    "root_chord": 6.86,  # meter
    "taper_ratio": 0.27,
    "LE_sweep": 39.2,  # deg
    "c/2_sweep": 35.02, # deg
}

# Parametric Description of Wingbox
WINGBOX = option_new_1

# Wingbox Material Parameters (in SI)
MAT = {
        "E": 68.9e9, # Pa
        "G": 26e9, # Pa
        "nu": 0.33,
        "sigma_y": 276e6, # Pa
    }

G = 9.80665 # m/s^2

# Critical Load Parameters (in SI)
CRIT = {
    "load_factor": 3.75,
    "distributed_loads": [(-199.8707 * G, 4355.183221 * G)],  # Wing Mass
    "point_loads": [(7277 * G, 8.374)],  # Engine Mass
    "point_torques": [
        (375000 * 2, 8.374)
    ],  # Engine Thrust (applied at 2 m from the centroid)
    "cld": 0.908,
    "dynp": 8328.245793,
}


