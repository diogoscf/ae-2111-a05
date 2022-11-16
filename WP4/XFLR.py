# Import ALL THE PACKAGES
import os
import scipy as sp
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate

# Imports data, change "MainWing_alpha_zero_v_ten.txt" to "FILENAMEHERE" to change files.
# Check is skip_header and skip_footer are appropriate in the new file. I think it'll be fine but just in case.

XFLR0_path = os.path.join(os.path.dirname(__file__), "./MainWing_alpha_zero_v_ten.txt")
XFLR10_path = os.path.join(os.path.dirname(__file__), "./MainWing_alpha_ten_v_ten.txt")
XFLRData_0 = np.genfromtxt(XFLR0_path, skip_header=40, skip_footer=1029)
XFLRData_10 = np.genfromtxt(XFLR10_path, skip_header=40, skip_footer=1029)


# Separates XFLRData into lists
y_lst = XFLRData_0[:, 0]
c_lst = XFLRData_0[:, 1]
cl_lst_0 = XFLRData_0[:, 3]
cd_lst_0 = XFLRData_0[:, 5]
cm_lst_0 = XFLRData_0[:, 7]
cl_lst_10 = XFLRData_10[:, 3]
cd_lst_10 = XFLRData_10[:, 5]
cm_lst_10 = XFLRData_10[:, 7]


def interpolater(y_pos, listtype):
    value = sp.interpolate.interp1d(
        y_lst, listtype, kind="cubic", fill_value="extrapolate"
    )
    value = value(abs(y_pos))
    return value
