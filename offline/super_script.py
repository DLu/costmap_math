#!/usr/bin/python

from functions import *
from djikstra import *
from metrics import all_metrics
import sys
import pylab
import matplotlib
from collections import defaultdict
from progressbar import *

OTHER_PARAMS = {'P': [0, 60, 50], 'N': [5, 100, 100], 'angle': [0, 90, 0], 
                'start': [0.0, 0.5, .1], 'goal':[0.1, .5, .1], 'obs':[0.1,0.5,0.5],
                'eight': [0,1,0], 'resolution': [2, 100, 10], 'resolution2': [2,100,10]}
SHORTCUT = True

WIDE = False

def get_args(oargs):
    G = globals().keys()[:]
    MAGIC = 'CMAP_'
    functions = [v[len(MAGIC):] for v in G if MAGIC in v]

    function_name = None
    for fne in functions:
        if fne in oargs:
            function_name = fne
            break
    if function_name is None:
        print "Function not specified!"
        print "Options are:"
        for fne in functions:
            print "\t%s"%fne
        exit(1)
          
    (function, args) = globals()[MAGIC + function_name]  
    params = {}
    unknowns = []
    
    for arg in oargs:
        if arg==function_name:
            continue
        elif ':' in arg:
            i = arg.index(':')
            name = arg[:i]
            value = arg[i+1:]
            if name in args or name in OTHER_PARAMS:
                params[name] = float(value)
            else:
                print "Unknown variable %s"%name
                exit(1)
        elif arg in args or arg in OTHER_PARAMS:
            unknowns.append(arg)
        else:
            print "Unknown argument %s"%arg
            exit(1)
            
    for name, (lo, hi, default) in args.items() + OTHER_PARAMS.items():
        if name in params:
            continue
        elif name in unknowns:
            params[name] = (lo, hi)
        else:
            params[name] = default
            
    return function, function_name, args, params, unknowns
    
def fractional_coordinates(N, fraction, angle):
    radius = N/2 - N * fraction
    rads = radians(angle)
    return int(N/2 - cos( rads ) * radius), int(N/2 + sin( rads ) * radius)

def super_path(function, args, params):
    N = int( params['N'] )
    if WIDE:
        g = make_grid(N*3, N)
    else:
        g = make_grid(N,N)
    fn_params = {}
    p_params = {}
    
    for param, value in params.iteritems():
        if param in args:
            fn_params[param] = value
            
    angle = params.get('angle', 0)
    sx, sy = fractional_coordinates(N, params.get('start', .1), angle)
    ex, ey = fractional_coordinates(N, params.get('goal', .1), angle+180)
    dx, dy = fractional_coordinates(N, params.get('obs', 0.0), angle)
    for (i,j) in g:
        g[ (i,j) ] = function(i,j,dx=-dx, dy=-dy, **fn_params)


    (score, path) = djikstra(g, (sx,sy), (ex,ey), constant=params['P'], neighbors=params['eight'])
    return g, score, path
    
def param_values((low, hi), resolution):
    d = hi - low
    values = []
    for i in range(int(resolution)):
        value = low + d * float(i) / (resolution - 1)
        values.append(value)
    return values
    
def clean_text(s):
    return ' '.join(s.split('_')).title()
    
def get_description(params, unknowns):
    desc = []
    for p,v in params.iteritems():
        if p in unknowns:
            continue
        elif p=='eight':
            if v==1.0:
                desc.append('EightConnected')
        elif p in ['resolution', 'angle', 'resolution2']:
            continue
        else:
            desc.append( '%s=%.1f'%(p,v) )
    return ', '.join(desc)   
    
def get_labels(array):
    N = len(array)
    if N<=5:
        return ([a+.5 for a in range(N)], array)
    else:
    
        return ( [0, N], [array[0], array[N-1]])
    
if __name__=='__main__':
    (function, name, args, params, unknowns) = get_args(sys.argv[1:])
    if len(unknowns)==0:
        # One path
        g, score, path = super_path(function, args, params)
        N = int( params['N'] )
        for m_name, metric in all_metrics:
            print m_name, metric(path, N)
        m = MapDrawer()
        m.data = g
        m.path = path
        m.draw()
    elif len(unknowns)==1:
        # graph
        resolution = params['resolution']


        param = unknowns[0]
        the_range = params[param]
        xs = param_values(the_range, resolution)
        ys = defaultdict(list)
        widgets = [Percentage(), ' ', Bar(marker='*',left='[',right=']'),' ', ETA()] 
        pbar = ProgressBar(widgets=widgets, maxval=len(xs))
        pbar.start()
        i = 0
        
        for value in xs:
            params[param] = value
            g, score, path = super_path(function, args, params)
            
            pbar.update(i)
            i += 1
            
            N = int( params['N'] )
            for m_name, metric in all_metrics:
                ys[m_name].append( metric(path, N) )

        desc = get_description(params, unknowns)
        for m_name in ys:
            pylab.plot(xs,ys[m_name], 'o-')
            pylab.xlabel(param)
            cm = clean_text(m_name)
            cn = clean_text(name)
            pylab.title('%s: %s\n%s'%(cm, cn, desc))
            fig = pylab.gcf()
            fig.canvas.set_window_title('%s - %s (%s)'%(cn, desc, cm))
            pylab.show()


    elif len(unknowns)==2:
        # heat map  
        resolution = params['resolution']
        resolution2 = params['resolution2']
        N = int( params['N'] )
        
        param, param2 = unknowns
        range1, range2 = params[param], params[param2]
        xs = param_values(range1, resolution)
        ys = param_values(range2, resolution2)
        print param, xs
        print param2, ys

        data = defaultdict(list)
        widgets = [Percentage(), ' ', Bar(marker='*',left='[',right=']'),' ', ETA()] 
        pbar = ProgressBar(widgets=widgets, maxval=len(xs)*len(ys))
        pbar.start()
        i = 0

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
                    
        colors = [('black')] + [(pylab.cm.jet(i)) for i in xrange(1,255)] + [('white')]
        new_map = matplotlib.colors.LinearSegmentedColormap.from_list('new_map', colors, N=256)
                    
        desc = get_description(params, unknowns)
        for m_name, metric in all_metrics:    
            cm = clean_text(m_name)
            cn = clean_text(name)
              
            mdata = pylab.array(data[m_name]) 
            pylab.pcolor(mdata, cmap=new_map)
            cbar = pylab.colorbar()
            cbar.set_label(cm)

            pylab.xlabel(param2)
            labels = get_labels(ys)
            pylab.xticks(labels[0], labels[1]) 
            
            pylab.ylabel(param)
            labels = get_labels(xs)
            pylab.yticks(labels[0], labels[1])
            
            pylab.title('%s: %s\n%s'%(cm, cn, desc))
            fig = pylab.gcf()
            fig.canvas.set_window_title('%s - %s (%s)'%(cn, desc, cm))

            if False:
                import os.path
                for d in range(500):
                    fn = "heatmap%03d.png"%d
                    if not os.path.exists(fn):
                        break
                    pylab.savefig(fn)
            else:
                pylab.show()
    else:
        print "Too Many Unknowns"
