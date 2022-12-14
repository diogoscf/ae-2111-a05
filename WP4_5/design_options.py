option_1 = {
    "front_spar": 0.2,
    "rear_spar": 0.65,
    "other_spars": [
        (0.3, 1),
        (0.35, 0.4),
        (0.45, 1),
        (0.5, 0.4),
        (0.6, 1),
    ],  # (x/c position value, y/(b/2) value of end of spar)
    "spar_thickness": (25e-3, 10e-3),  # (t_root, t_tip) interpolated linearly. [meter]
    "skin_thickness": 10e-3,  # meter
    "stringer_area": 480e-6,  # square meter
    "stringers_top": [(50, 0.4), (40, 0.65), (20, 1)],  # *Ordered* List: (nstringers, y/(b/2) value of end) - start is end of previous or root
    "stringers_bottom": [(50, 0.4), (40, 0.65), (20, 1)],  # same as above
    "ribs": (0, 0.4, 0.65, 1), # y/(b/2) values of rib positions
}

option_2 = {
    "front_spar": 0.2,
    "rear_spar": 0.65,
    "other_spars": [
        (0.3, 0.4),
        (0.4, 1),
        (0.5, 0.4),
    ],  # (x/c position value, y/(b/2) value of end of spar)
    "spar_thickness": (25e-3, 10e-3),  # (t_root, t_tip) interpolated linearly. [meter]
    "skin_thickness": 21e-3,  # meter
    "stringer_area": 80e-6,  # square meter
    "stringers_top": [(10, 1)],  # *Ordered* List: (nstringers, y/(b/2) value of end) - start is end of previous or root
    "stringers_bottom": [(10, 1)],  # same as above
    "ribs": (0, 0.4, 0.65, 1), # y/(b/2) values of rib positions
}

option_3 = {
    "front_spar": 0.2,
    "rear_spar": 0.65,
    "other_spars": [
        (0.25, 0.4),
        (0.3, 1),
        (0.35, 0.4),
        (0.4, 1),
        (0.45, 0.4),
        (0.5, 1),
        (0.55, 0.4),
        (0.6, 0.4),
    ],  # (x/c position value, y/(b/2) value of end of spar)
    "spar_thickness": (37.5e-3, 15e-3),  # (t_root, t_tip) interpolated linearly. [meter]
    "skin_thickness": 10e-3,  # meter
    "stringer_area": 480e-6,  # square meter
    "stringers_top": [(30, 0.4), (20, 0.65), (10, 1)],  # *Ordered* List: (nstringers, y/(b/2) value of end) - start is end of previous or root
    "stringers_bottom": [(30, 0.4), (20, 0.65), (10, 1)],  # same as above
    "ribs": (0, 0.4, 0.65, 1), # y/(b/2) values of rib positions
}