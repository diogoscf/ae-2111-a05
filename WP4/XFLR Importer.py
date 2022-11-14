
#Import ALL THE PACKAGES
import scipy as sp
import numpy as np 
import matplotlib.pyplot as plt 
from scipy import interpolate

#Imports data, change "MainWing_alpha_zero_v_ten.txt" to "FILENAMEHERE" to change files.
#Check is skip_header and skip_footer are appropriate in the new file. I think it'll be fine but just in case.
XFLRData = np.genfromtxt("MainWing_alpha_zero_v_ten.txt", skip_header=40, skip_footer=1029)
#Separates XFLRData into lists
y_lst = XFLRData[:,0]
c_lst = XFLRData[:,1]
cl_lst = XFLRData[:,3]
cd_lst = XFLRData[:,5]
cm_lst = XFLRData[:,7]

#List interpolater
#def cl_interpolater(y_pos):
y_pos=10
cl_value = sp.interpolate.interpld(y_lst, cl_lst, kind='cubic', fill_value="extrapolate")
cl_value = cl_value(y_pos)
    
#cl_interpolater(10)    
print(cl_value)