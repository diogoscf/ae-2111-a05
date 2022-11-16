import numpy as np
'''
- the constants a,b,c,d,e,f,g is the length of each components of the wing box.
- q1 is the shear flow in the left cell
- q2 is the shear flow in the right cell
- t1 is the thickness of the spar
- t2 is the thickness along the lines that connects the spar
- A1 is the enclosed area of the left cell
- A2 is the enclosed area of the right cell
'''

'''
#Formula for the torque
def T(A1, q1, A2, q2): #T is torque
    T = 2*A1*q1 + 2*A2*q2
    return T
    
#dtheta/dy over left cell
def dtheta_dy1(A1,G,q1,q2,a,b,g,f,t1,t2):
    dtheta_dy1 = 1/(2*A1*G) * (((q1-q2)*g/t1)+((q1*f)/t2)+((q1*a)/t1)+((q1*b)/t2))
    return dtheta_dy1

#dtheta/dy over right shell
def dtheta_dy2(A2,G,q1,q2,c,d,e,g,t1,t2):
    dtheta_dy2 = 1/(2*A2*G) * ((q2*c/t2)+(q2*d/t1)+(q2*e/t2)+((q2-q1)*g/t1))
    return dtheta_dy2
'''

def solve_three_eq(A1,A2,t1,t2,a,b,c,d,e,f,g,T):
    matrix = np.array([2*A1, 2*A2,0],[((a+g)/t1)+((b+f)/t2),g/t1,-2*A1*G],[g/t1,((c+e)/t2)+((d+g)/t1),2*A2*G])
    righthandside = np.array([T,0,0])
    solution = np.linalg.solve(matrix,righthandside)
    q1 = solution[0]
    q2 = solution[1]
    dtheta_dy = solution[2]
    return q1, q2, dtheta_dy
