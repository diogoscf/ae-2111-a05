import numpy as np
import scipy as sp
from scipy import integrate
import Distributions
import matplotlib.pyplot as plt
from math import sin, cos, pi


def normal_force_per_span(lift_per, drag_per, angle_of_attack):
    return cos(angle_of_attack) * lift_per + sin(angle_of_attack) * drag_per


def shear_force_diagram(cl_d):
    y_tab = []
    x_tab = []
    cl_min = 0
    cl_max = 1.5
    y_pos = np.linspace(-22, 22, 100)
    for i in range(len(y_pos) - 1):
        y_tab.append(
            normal_force_per_y := normal_force_per_span(
                Distributions.L_prime(cl_d, y_pos[i], Distributions.dyn_p),
                Distributions.D_prime(
                    0.028 + cl_d**2 / (pi * 10 * 0.51), y_pos[i], Distributions.dyn_p
                ),
                Distributions.AOA_specific_flight_regime(cl_d),
            )
        )
        x_tab.append(y_pos[i])

    print(y_tab)
    plt.plot(x_tab, y_tab)
    plt.title(f"Shear force at a cl of {cl_d}")
    plt.show()


shear_force_diagram(0)
