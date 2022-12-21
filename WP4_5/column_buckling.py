import numpy as np
import matplotlib.pyplot as plt
from math import pi
import scipy as sp
from scipy import interpolate
from params import *
from compression_failure import *
from design_options import *

#numbers below are arbitrary
STRINGER = {
    "vertical_l": 60, #mm
    "thickness": 6, #mm
    "E_AL6061-T6": 68.9*10**9 #Pa
}

#option=[option_1,option_2,option_3] #WP4 designs
option=WINGBOX #current design

#area of one stringer
vl=STRINGER["vertical_l"]
t=STRINGER["thickness"]
A=vl**2/5
#print('stringer area:',A, 'mm^2')

Ribs_pos=WINGBOX["ribs"]# -> 0.4 and 0.65
#Ribs_pos=option[0]["ribs"]
#Ribs_pos=(0,0.05,0.1,0.15,0.21,0.27,0.33,0.4,0.47,0.56,0.65,0.79,1)
Index=range(0,len(Ribs_pos))

def Ixx(t,Lv): #of one stringer
    t=float(t)
    Lv=float(Lv)
    y=(0.5*Lv*Lv*t)/(Lv*t+Lv*t)

    Ixx= Lv*t*y**2 + 1/12*t*Lv**3 + Lv*t*(0.5*Lv-y)**2
    return Ixx

#o crit of segment @ y/(b/2) for chosen design
def crit_buckling_str(y):
  
    g=sp.interpolate.interp1d(Ribs_pos,Index,kind="next",fill_value="extrapolate")
    L= (Ribs_pos[int(g(y))]-Ribs_pos[int(g(y)-1)])*(WING["span"]*1000)/2 #mm; unsupported length
    E= STRINGER["E_AL6061-T6"]
    K=4 #assume rib at the very end
    I=Ixx(t,vl) 

    o_cr= (K*pi**2*E*I)/(L**2*A) *10**-6 #MPa
    return o_cr


#applied stress
y_lst=[]
sigma_y_lst=[]
o_cr_lst=[]
y=0
dy=1/300
for i in range(0,300):
    sigma_y_lst.append(sigma_y(y,option))
    o_cr_lst.append(crit_buckling_str(y))
    y_lst.append(y*WING["span"]/2)
    y=y+dy

sigma_y_lst=np.array(sigma_y_lst)
o_app_lst=np.divide(sigma_y_lst,-1000000)
o_cr_lst=np.array(o_cr_lst)

#margin of safety & plot
m_of_s=np.divide(o_cr_lst,o_app_lst)

def plot_m_of_s():

    plt.subplot(121)
    plt.plot(y_lst,m_of_s)
    plt.ylabel("Margin of safety")
    plt.xlabel("Half wing span (y position)")
    plt.axhline(y=1, color='r', linestyle='-')
#    plt.xlim([0,20]) #so far it is reasonable only for small y distances 
    plt.ylim([0,4]) #past some point (~17m) mos goes really high (because loads are very small?)
    plt.grid(True)

    plt.subplot(122)
    plt.plot(y_lst,o_app_lst)
    plt.plot(y_lst,o_cr_lst)
    plt.legend(('Applied','Critical'))
    plt.xlabel("Half wing span [m]")
    plt.grid(True)

    plt.show()

plot_m_of_s()
