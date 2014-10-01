
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


for i, x in enumerate(xs):
    a = []
    for j, y in enumerate(ys):
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
labels = get_labels(ys)
pylab.xticks(labels[0], labels[1]) 

pylab.ylabel('Variance')
labels = get_labels(xs)
pylab.yticks(labels[0], labels[1])

#pylab.title('%s: %s\n%s'%(cm, cn, desc))
fig = pylab.gcf()
#fig.canvas.set_window_title('%s - %s (%s)'%(cn, desc, cm))

pylab.show()
"""

        for v1 in xs:
            params[param] = v1
            for m_name, metric in all_metrics:
                data[m_name].append([])

            maxxed = False
            last = None
            for v2 in ys:
                pbar.update(i)
                i += 1
                params[param2] = v2
                if maxxed:
                    g, score, path = last
                else:
                    g, score, path = super_path(function, args, params)
                    last = g,score,path
                for m_name, metric in all_metrics:
                    value = metric(path, N)
                    if SHORTCUT and value==0 and m_name=='closest_distance':
                        maxxed = True
                    data[m_name][-1].append( value )

        pbar.finish()
                    
        
                """
