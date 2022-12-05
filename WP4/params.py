# Wing Parametric Description (values in SI)
WING = {
    "span": 43.58,  # meter
    "root_chord": 6.86,  # meter
    "taper_ratio": 0.27,
    "LE_sweep": 39.2,  # deg
}

# Parametric Description of Wingbox
WINGBOX = {
    "front_spar": 0.2,
    "rear_spar": 0.65,
    "other_spars": [
        (0.25, 0.5),
        (0.3, 1),
        (0.4, 0.4),
        (0.5, 0.5),
    ],  # (x/c position value, y/(b/2) value of end of spar)
    "spar_thickness": (12e-3, 10e-3),  # (t_root, t_tip) interpolated linearly. [meter]
    "skin_thickness": (10e-3, 7e-3),  # (t_root, t_tip) interpolated linearly. [meter]
    "stringer_area": 60e-6,  # square meter
    "stringers_top": [(0, 0.4), (0, 0.7), (0, 1)],  # *Ordered* List: (nstringers, y/(b/2) value of end) - start is end of previous or root
    "stringers_bottom": [(0, 0.4), (0, 0.7), (0, 1)],  # same as above
}

# Wingbox Material Parameters (in SI)
MAT = {"E": 68.9e9, "G": 26e9}  # pascal  # pascal

G = 9.80665

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
