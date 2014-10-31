from math import *

def none(x, y, dx=0, dy=0):
    x += dx
    y += dy
    h = sqrt(x*x+y*y)
    if h < 6:
        return 100
    return 0.0

CMAP_none = (none, {})

def gaussian(x, y, dx=0, dy=0, A=99, var=100, var2=None):
    bv = none(x,y,dx,dy)
    if var2 is None:
        var2 = var
    x += dx
    y += dy
    h = sqrt(x*x+y*y)
    angle = atan2(y,x)
    mx = cos(angle) * h
    my = sin(angle) * h
    f1 = pow(mx, 2.0)/(2.0 * var)
    f2 = pow(my, 2.0)/(2.0 * var2)
    return max(A * exp(-(f1 + f2)), bv)
    
CMAP_gaussian = (gaussian, {'A':[0,100,99], 'var':[1,400,100]})

def two_gaussians(x, y, dx=0, dy=0, A1=50, A2=40, var1=100, var2=100):
    return max(gaussian(x,y,dx,dy,A1,var1) , gaussian(x,y,dx,dy,A2,var2))

CMAP_two_gaussians = (two_gaussians, {'A1':[0,100,50], 'var1':[1,400,100], 'A2':[0,100,40], 'var2':[1,400,100]})

def svenstrup(x,y,dx=0,dy=0):
    A = -gaussian(x,y,dx,dy,var=75)
    B = 0
    if y > -dy:
        B = gaussian(x,y,dx,dy,var=20,var2=10)
    return A + B


def linear(x, y, dx=0, dy=0, A=99, slope=1, power=2):
    x += dx
    y += dy
    d = sqrt(pow(x,2)+pow(y,2))
    return max(A-pow(d,power)*slope, 0)
    
CMAP_distance = (linear, {'A':[0,100, 99], 'slope':[0.1, 10, 1], 'power':[1,10,2]})

def inverse(x, y, dx=0, dy=0, A=99, factor=1, power=1, addend=1):
    x += dx
    y += dy
    d = sqrt(pow(x,2)+pow(y,2))
    return A / (factor * pow(d,power) + addend)
    
CMAP_inverse = (inverse, {'A': [0, 100, 99], 'factor':[.01,.1,.1], 'power':[1,5,1]})

def constant(x, y, dx=0, dy=0, A=50, xd=5, yd=5):
    x += dx
    y += dy
    if abs(x)<=xd and abs(y)<=yd:
        return A
    else:
        return 0
        
CMAP_constant = (constant, {'A': [0, 100, 20], 'xd': [0, 20, 5], 'yd': [0, 50, 5]})



def gaussianc(x, y, dx=0, dy=0, A=99, var=100, var2=None, c=.1):
    bv = 0 * none(x,y,dx,dy)
    if var2 is None:
        var2 = var
    x += dx
    y += dy
    h = sqrt(x*x+y*y)
    angle = atan2(y,x)
    mx = cos(angle) * h
    my = sin(angle) * h
    f1 = pow(mx, 2.0)/(2.0 * var)
    f2 = pow(my, 2.0)/(2.0 * var2)
    return max(A * exp(-(f1 + f2)), bv) + c
    
CMAP_gaussianc = (gaussianc, {'A':[0,100,99], 'var':[1,400,100], 'c':[0,10,10]})
