import numpy as np
import scipy as sp
from scipy import integrate

def normal_force_per_span(lift_per, drag_per, angle_of_attack):
    return cos(angle_of_attack) * lift_per + sin(angle_of_attack) * drag_per


def shear_force_diagram():
    y_pos = np.linspace(-22, 22, 100)
    for i in range(len(y_pos) - 1):

