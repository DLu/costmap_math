#!/usr/bin/python

from numpy import arange
from costmap_math.tfpub import *
from costmap_math.people import *
from costmap_math.map_gen import *
from navfn.srv import *
import dynamic_reconfigure.client
import numpy

SERVICE_NAME = '/global_planner/make_plan'

L = 16

class CostmapMath:
    def __init__(self):
        rospy.init_node('costmap_math')
        self.tf = TFPub()
        self.people = PeoplePub()
        self.map = MapGen()
        self.map.publish(L,1.5)
        rospy.wait_for_service(SERVICE_NAME)
        self.planner = rospy.ServiceProxy(SERVICE_NAME, MakeNavPlan)
        
        self.cparams = dynamic_reconfigure.client.Client('/global_planner/costmap/social')
        self.pparams = dynamic_reconfigure.client.Client('/global_planner/planner')
        
    def plan(self, x=2.0):
        self.tf.x = -x
        req = MakeNavPlanRequest()
        req.start.header.frame_id = '/map'
        req.start.pose.position.x = -x
        req.start.pose.orientation.w = 1.0
        req.goal.header.frame_id = '/map'
        req.goal.pose.position.x = x
        req.goal.pose.orientation.w = 1.0
        
        resp = self.planner(req)
        path = []
        for pt in resp.path:
            path.append( (pt.pose.position.x, pt.pose.position.y) )
        return path
        
import pickle, os.path, collections
import sys


KEY = 'OPEN'

N = 1

c = CostmapMath()


if '-m' in sys.argv:
    while not rospy.is_shutdown():
        path = c.plan(L/2-1)
        rospy.sleep(1)
else:
    if os.path.exists('data.pickle'):
        data = pickle.load(open('data.pickle'))
    else:
        data = collections.defaultdict(list)
    print 'loaded'

    #P = rospy.get_param('/global_planner/planner/neutral_cost')
    #for amp in arange(0, 200, 5):
    for trial in range(N):
        amp = 80.0
        #for ratio in arange(0, 48.1, 4):
        #    if ratio==0.0:
        #        continue
        #    amp = P / ratio
        for P in arange(0.0, 80.1, 5):
            c.pparams.update_configuration({'neutral_cost': P})
            for var in arange(0, 20.1, 5.0):
                key = (KEY, P, var)
                if len(data[key]) > trial:
                    print "Skip", amp, var, P, trial+1
                    continue
                print amp, var, P, (trial+1)
                c.cparams.update_configuration({'amplitude': amp, 'covariance': var})
                rospy.sleep(1)
                path = c.plan(4)
                rospy.sleep(1)
                if len(path)==0:
                    continue
                data[key].append(path)
            
    pickle.dump(data, open('data.pickle', 'w'))
    print "DONE"
    rospy.spin()

