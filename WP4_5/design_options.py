import numpy as np
import copy

# nsparlist e.g. [(10, 0.4), (5, 0.65), (2, 1)]
def distspars(nsparlist):
    n = nsparlist[0][0] - 2
    spars = [[0.2 + (0.45/(n+1))*(i+1), 1] for i in range(n)]
    remaining = [i for i in range(n)]
    rmv = []
    for prev, curr in zip(nsparlist, nsparlist[1:]):
        diff = prev[0] - curr[0]
        jump = prev[0] // diff if diff != 0 else 0
        #print("CHANGE", prev[0], curr[0], jump, diff)
        tmp = copy.deepcopy(remaining)
        j = 0
        for i in range(diff):
            #k = int((np.ceil(rmv / 2))) + (i // 2) if i % 2 == 0 else -((i+1) // 2) - int((np.floor(rmv / 2)))
            factor = 1 if i % 2 == 0 else -1
            if i % 2 == 1: j += jump
            k = remaining[j*factor]
            while k in rmv:
                if k < n-1:
                    k += 1
                else:
                    k = 0
            #print(i, factor, j, k)
            tmp.pop(tmp.index(k))
            spars[k][1] = prev[1]
            rmv.append(k)

        remaining = tmp
    return spars

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

option_new_s = {
    "front_spar": 0.2,
    "rear_spar": 0.65,
    "other_spars": [
        (0.3, 1),
        (0.4, 1),
        (0.5, 1),
    ],  # (x/c position value, y/(b/2) value of end of spar)
    "spar_thickness": (37.5e-3, 15e-3),  # (t_root, t_tip) interpolated linearly. [meter]
    "skin_thickness": 20e-3,  # meter
    "stringer_area": 720e-6,  # square meter
    "stringers_top": [(20, 1),],  # *Ordered* List: (nstringers, y/(b/2) value of end) - start is end of previous or root
    "stringers_bottom": [(20, 1),],  # same as above
    "ribs": (0, 0.1, 0.2, 0.4, 0.52, 0.65, 0.85, 0.9, 1), # y/(b/2) values of rib positions
}

option_new_1 = {
    "front_spar": 0.2,
    "rear_spar": 0.65,
    "other_spars": distspars([(7, 0.2), (3, 0.4)]),  # (x/c position value, y/(b/2) value of end of spar)
    "spar_thickness": (37.5e-3, 15e-3),  # (t_root, t_tip) interpolated linearly. [meter]
    "skin_thickness": 39e-3,  # meter
    "stringer_area": 720e-6,  # square meter
    "stringers_top": [(18, 0.2), (10, 0.4), (1, 0.65)],  # *Ordered* List: (nstringers, y/(b/2) value of end) - start is end of previous or root
    "stringers_bottom": [(18, 0.2), (10, 0.4), (1, 0.65)],  # same as above
    "ribs": (0, 0.1, 0.2, 0.3, 0.4, 0.52, 0.65, 0.75, 0.85, 0.9, 1), # y/(b/2) values of rib positions
}

option_new_2 = {
    "front_spar": 0.2,
    "rear_spar": 0.65,
    "other_spars": distspars([(21, 0.2), (15, 0.4), (8, 0.52), (2, 0.65), (2, 1)]),  # (x/c position value, y/(b/2) value of end of spar)
    "spar_thickness": (37.5e-3, 15e-3),  # (t_root, t_tip) interpolated linearly. [meter]
    "skin_thickness": 24e-3,  # meter
    "stringer_area": 720e-6,  # square meter
    "stringers_top": [(20, 0.2), (14, 0.4), (7, 0.52), (3, 0.65), (1, 0.85)],  # *Ordered* List: (nstringers, y/(b/2) value of end) - start is end of previous or root
    "stringers_bottom": [(20, 0.2), (14, 0.4),(7, 0.52), (3, 0.65), (1, 0.85)],  # same as above
    "ribs": (0, 0.1, 0.2, 0.3, 0.4, 0.52, 0.65, 0.75, 0.85, 0.9, 1), # y/(b/2) values of rib positions
}