from functions import *
from pylab import *
import sys
P = float(sys.argv[1])
N = 500

def f(x,y):
    return gaussian(x,y, dy=-N/2, A=50)

xs = range(0,30)
As = []
bs = []
cs = []
ys = []
for x in xs:
    a = sum([f(i,0)+f(i,N) for i in range(0, x)])
    b = 2 * x * P
    c = sum([f(x,y) for y in range(N+1)])
    As.append(a)
    bs.append(b)
    cs.append(a+c)
    v = a + b + c
    ys.append(v)
    
#plot(xs, As, label="A")
plot(xs, bs, label="Step cost")
plot(xs, cs, label="Gaussian cost")
plot(xs, ys, label="Total cost")
ylim([0, 2500])
legend(loc=2)
show()
