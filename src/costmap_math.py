#!/usr/bin/python

from numpy import arange
from costmap_math.tfpub import *
from costmap_math.people import *
from costmap_math.map_gen import *
from navfn.srv import *
import dynamic_reconfigure.client
import numpy

SERVICE_NAME = '/global_planner/make_plan'

class CostmapMath:
    def __init__(self):
        rospy.init_node('costmap_math')
        self.tf = TFPub()
        self.people = PeoplePub()
        self.map = MapGen()
        self.map.publish()
        rospy.wait_for_service(SERVICE_NAME)
        self.planner = rospy.ServiceProxy(SERVICE_NAME, MakeNavPlan)
        
        self.params = dynamic_reconfigure.client.Client('/global_planner/costmap/social')
        
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
        
import pickle
data = pickle.load(open('data.pickle'))
print 'loaded'
KEY = 'OPEN'
c = CostmapMath()
for amp in arange(0, 200, 10):
    for var in arange(0, 5, 1.5):
        key = (KEY, amp, var)
        if key in data:
            continue
        c.params.update_configuration({'amplitude': amp, 'covariance': var})
        rospy.sleep(1.0)
        path = c.plan(4)
        data[key] = path
        
pickle.dump(data, open('data.pickle', 'w'))
print "DONE"
rospy.spin()

