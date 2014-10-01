#!/usr/bin/python

import rospy
from costmap_math.tfpub import *
from costmap_math.people import *
from costmap_math.map_gen import *
from navfn.srv import *
import dynamic_reconfigure.client

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
        self.params.update_configuration({'covariance': 1.42})
        
        print "GO"
        self.plan()
        
    def plan(self):
        req = MakeNavPlanRequest()
        req.start.header.frame_id = '/map'
        req.start.pose.position.x = -2
        req.start.pose.orientation.w = 1.0
        req.goal.header.frame_id = '/map'
        req.goal.pose.position.x = 2
        req.goal.pose.orientation.w = 1.0
        
        resp = self.planner(req)
        path = []
        for pt in resp.path:
            path.append( (pt.pose.position.x, pt.pose.position.y) )
        print path
        
c = CostmapMath()
rospy.spin()
        
