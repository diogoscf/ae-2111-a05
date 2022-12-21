import numpy as np
import matplotlib.pyplot as plt
from math import pi
import scipy as sp
from scipy import interpolate
from params import *
#from compression_failure import * #with stresses from Tim
from stresses import * #with stresses from Diogo
from design_options import *

STRINGER = {
    "vertical_l": 60, #mm
    "horizontal_l": 60, #mm
    "thickness": 6, #mm
    "E_AL6061-T6": 68.9*10**9 #Pa
}

#option=[option_1,option_2,option_3] #WP4 designs
option=WINGBOX #current design

#area of one stringer
vl,hl=STRINGER["vertical_l"],STRINGER["horizontal_l"]
t=STRINGER["thickness"]
A=vl*t+hl*t
#print('stringer area:',A, 'mm^2')

Ribs_pos=WINGBOX["ribs"]# -> 0.4 and 0.65
#Ribs_pos=option[0]["ribs"]  
#Ribs_pos=(0, 0.06 ,0.13, 0.2, 0.27, 0.35, 0.4 ,0.52, 0.65, 0.75, 0.85, 0.9, 1)
Index=range(0,len(Ribs_pos))

def Ixx(t,Lv,Lh): #of one stringer
    t=float(t)
    Lh=float(Lh)
    Lv=float(Lv)
    y=(0.5*Lv*Lv*t)/(Lh*t+Lv*t)

    Ixx= Lh*t*y**2 + 1/12*t*Lv**3 + Lv*t*(0.5*Lv-y)**2
    return Ixx

#o crit of segment @ y/(b/2) for chosen design
def crit_buckling_str(y):
  
    g=sp.interpolate.interp1d(Ribs_pos,Index,kind="next",fill_value="extrapolate")
    L= (Ribs_pos[int(g(y))]-Ribs_pos[int(g(y)-1)])*(WING["span"]*1000)/2 #mm; unsupported length
    E= STRINGER["E_AL6061-T6"]
    K=4 #assume rib at the very end
    I=Ixx(t,vl,hl) 

    o_cr= (K*pi**2*E*I)/(L**2*A) *10**-6 #MPa
    return o_cr


#applied stress
y_lst=[]
sigma_y_lst=[]
o_cr_lst=[]
y=0
dy=1/300
for i in range(0,300):
   # sigma_y_lst.append(sigma_y(y,option))
    o_cr_lst.append(crit_buckling_str(y))
    y_lst.append(y*WING["span"]/2)
    y=y+dy

y_lst=np.array(y_lst)
y_lst=np.delete(y_lst,0)
y_lst=np.delete(y_lst,-1)

#sigma_y_lst=np.array(sigma_y_lst)
#sigma_y_lst=np.delete(sigma_y_lst,0)
#o_app_lst=np.divide(sigma_y_lst,-1000000) #turn to Mpa
sigma_y_lst=stresses_along_wing(CL_d, point_loads, distributed_loads, load_factor, dynp, wbox = design_options.option_new_1)
o_app_lst=np.divide(sigma_y_lst[:,0],-1)
o_app_lst=np.delete(o_app_lst,0)
o_app_lst=np.delete(o_app_lst,-1)

o_cr_lst=np.array(o_cr_lst)
o_cr_lst=np.delete(o_cr_lst,0)
o_cr_lst=np.delete(o_cr_lst,-1)

#margin of safety & plot
m_of_s=np.divide(o_cr_lst,o_app_lst)

def plot_m_of_s():

    plt.subplot(121)
    plt.plot(y_lst,m_of_s)
    plt.ylabel("Margin of safety")
    plt.xlabel("Half wing span (y position)")
    plt.axhline(y=1, color='r', linestyle='-') 
    plt.ylim([0,4])
    plt.grid(True)

    plt.subplot(122)
    plt.plot(y_lst,o_app_lst)
    plt.plot(y_lst,o_cr_lst)
    plt.legend(('Applied','Critical'))
    plt.xlabel("Half wing span [m]")
    plt.grid(True)

    plt.show()

plot_m_of_s()
