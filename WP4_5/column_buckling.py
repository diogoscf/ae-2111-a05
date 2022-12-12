import numpy as np
import matplotlib.pyplot as plt
from math import pi
import scipy as sp
from scipy import interpolate
from params import *
from compression_failure import *

#numbers below are arbitrary
STRINGER = {
    "vertical_l": 100, #mm
    "horizontal_l": 100, #mm
    "thickness": 5, #mm
    "number": [60,40,20],
    "area_(wanted)": 480, #mm^2
    "E_AL6061-T6": 68*10**9 #Pa
}

#code for producing moment of inertia vs thickness
'''
vertical_l = L
horizontal_l = b
thickness = t
number = N
area_(wanted) = A


#calculation in mm
def MOI(t,A):
    t = float(t)
    A = float(A)
    b = 10*t
    L = (10*A/b)-b
    MOI_ind = (b*t*(L**2/(0.5*(L+b)))**2) + (0.5*t*L**3) + (L**2*t/2)+(L*t/4*((L**2)/(L+b))**2) + ((b*t + L*t)*(0.5*(L**2 + b*t)/(L+b))**2)
    return MOI_ind

xtab = []
y1tab = []
for t in np.arange(0.1,20,0.2):
    xtab.append(t)
    y1 = MOI(t,4.8) #Assumed the total area is 480 [mm] and 100 stringer is used so the individual stringer's area is 4.8
    y1tab.append(y1)

plt.plot(xtab,y1tab)
plt.show()
print(y1tab)
'''
#area of one stringer
vl,hl=STRINGER["vertical_l"],STRINGER["horizontal_l"]
t=STRINGER["thickness"]
A=vl*t+(hl-t)*t
#print(A)

#Design options [spar thickness(root,tip), skin thickness, stringer area, spar nr, stringer nr]
D1= [(25,10), 10, 480, (7,5), (100,80,40)]
D2= [(25,10), 21, 80, (5,3), (20,20,20)]
D3= [(37.5,15), 15, 480, (10,5), (60,40,20)]

Ribs_pos=[0,0.1,0.2,0.3,0.4,1]
Index=[0,1,2,3,4,5]

def Ixx(t,Lv,Lh): #of one stringer
    t=float(t)
    Lh=float(Lh)
    Lv=float(Lv)
    y=(0.5*Lv*Lv*t)/(Lh*t+Lv*t)

    Ixx= Lh*t*y**2 + 1/12*t*Lv**3 + Lv*t*(0.5*Lv-y)**2
    return Ixx
 
#print(Ixx(t,vl,hl))
    

#o crit of segment @ y/(b/2) for chosen design
def crit_buckling_str(y):        
    g=sp.interpolate.interp1d(Ribs_pos,Index,kind="next",fill_value="extrapolate")
    L= (Ribs_pos[int(g(y))]-Ribs_pos[int(g(y)-1)])*(WING["span"]*1000)/2 #mm; unsupported length
    E= STRINGER["E_AL6061-T6"]
    K=4 #assume rib at the very end
    I=Ixx(t,vl,hl) 
    
    o_cr= (K*pi**2*E*I)/(L**2*A) *10**-6 #MPa
    return o_cr
    
#print(crit_buckling_str(0.3),"MPa")

#applied stress
o_cr_lst=[]
y_lst=[]

def sigma_y_lst():
    y=0
    i=0
    a=0
    sigma_y_lst=[]
    y_lst=[]
    while i <=300 and a<=1:
        a= sigma_y(y)
        i+=1
        sigma_y_lst.append(a)
        y_lst.append(y*halfspan)
        y+=1/300
    sigma_y_lst=np.array(sigma_y_lst)
    sigma_y_lst=sigma_y_lst/-10**6
    return sigma_y_lst

o_app_lst=np.delete(sigma_y_lst(),-1)
#o_app_lst=np.array(o_app_lst)
#print(o_app_lst)
#print(len(o_app_lst))

dy=1/len(o_app_lst)
y=0
for i in range(0,len(o_app_lst)):
    o_cr_lst.append(crit_buckling_str(y))
    y_lst.append(y*WING["span"]/2)
    y=y+dy
  
o_cr_lst=np.array(o_cr_lst)
#print(o_cr_lst)
#print(y_lst)

#margin of safety & plot
m_of_s=np.divide(o_cr_lst,o_app_lst)
#print(m_of_s)

#plot graphs
plt.plot(y_lst,m_of_s)
plt.xlabel("Half wing span (y position)")
plt.ylabel("Margin of safety")
plt.xlim([0,6]) #so far it is reasonable only for small y distances 
plt.ylim([0,5]) #past some point (~15m) mos goes really high
plt.show()
