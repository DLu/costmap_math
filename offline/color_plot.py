from functions import *
import pylab
import matplotlib

N = 50
g = []

for i in range(N):
    a = []
    for j in range(N):
        x = svenstrup(i,j,dx=-N/2, dy=-N/2)
        a.append(x)
    g.append(a)


colors = [('black')] + [(pylab.cm.jet(i)) for i in xrange(1,255)] + [('white')]
new_map = matplotlib.colors.LinearSegmentedColormap.from_list('new_map', colors, N=256)

mdata = pylab.array(g) 
pylab.pcolor(mdata, cmap=new_map)
cbar = pylab.colorbar()


pylab.show()
