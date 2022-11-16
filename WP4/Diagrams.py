import numpy as np
import scipy as sp
from scipy import integrate
import Distributions
import matplotlib.pyplot as plt
from math import sin, cos, pi


def normal_force_per_span(lift_per, drag_per, angle_of_attack):
    return cos(angle_of_attack) * lift_per + sin(angle_of_attack) * drag_per


def shear_force_diagram(cl_d):
    cl_min = 0
    cl_max = 1.5
    y_pos = np.linspace(0, 22, 100)
    normal = Distributions.N_prime(
        cl_d, 0.028 + cl_d**2 / (pi * 10 * 0.51), y_pos, Distributions.dyn_p
    )

    plt.plot(y_pos, normal)
    plt.title(f"Shear force at a cl of {cl_d}")
    plt.show()


shear_force_diagram(0)
