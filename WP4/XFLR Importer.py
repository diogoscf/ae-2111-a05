import scipy as sp
import numpy as np 
#Imports data
XFLRData = np.genfromtxt("MainWing_alpha_zero_v_ten.txt", skip_header=40, skip_footer=1029)
y_lst = XFLRData[:,0]
c_lst = XFLRData[:,1]
cl_lst = XFLRData[:,3]
cd_lst = XFLRData[:,5]
cm_lst = XFLRData[:,7]
print(cm_lst)

def 