
import pylab
import matplotlib
from collections import defaultdict
import pickle

def get_labels(array):
    N = len(array)
    if N<=5:
        return ([a+.5 for a in range(N)], array)
    else:
    
        return ( [0, N], [array[0], array[N-1]])

paths = pickle.load(open('data.pickle'))
xs = set()
ys = set()
for key, amp, var in paths:
    xs.add( amp )
    ys.add( var )
    
metrics = []

xs = sorted(list(xs))
ys = sorted(list(ys))


for j, y in enumerate(ys):
    a = []
    for i, x in enumerate(xs):
        K = (key,x,y)
        if K in paths and len(paths[K])>0: 
            path = paths[ K ]
            ym = max( [abs(yy) for xx,yy in path] )
            a.append(ym)
        else:
            a.append(0.0)
    metrics.append(a)
    
    
    
colors = [('black')] + [(pylab.cm.jet(i)) for i in xrange(1,255)] + [('white')]
new_map = matplotlib.colors.LinearSegmentedColormap.from_list('new_map', colors, N=256)
                    
mdata = pylab.array(metrics) 
pylab.pcolor(mdata, cmap=new_map)
cbar = pylab.colorbar()
#cbar.set_label(cm)

pylab.xlabel('Amplitude')
labels = get_labels(xs)
pylab.xticks(labels[0], labels[1]) 

pylab.ylabel('Variance')
labels = get_labels(ys)
pylab.yticks(labels[0], labels[1])

#pylab.title('%s: %s\n%s'%(cm, cn, desc))
fig = pylab.gcf()
#fig.canvas.set_window_title('%s - %s (%s)'%(cn, desc, cm))

pylab.show()

