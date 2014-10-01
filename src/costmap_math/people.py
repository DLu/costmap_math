#!/usr/bin/python

import rospy
import threading
from people_msgs.msg import Person, People

class PeoplePub:
    def __init__(self):
        self.ppub = rospy.Publisher('/people', People)
        self.x = 0.0
        self.y = 0.0
        
        self.t = threading.Thread(target=self.spin)
        self.t.start()

    def spin(self):
        rate = rospy.Rate(10)
        while not rospy.is_shutdown():
            pv = Person()
            pl = People()
            pl.header.stamp = rospy.Time.now()
            pl.header.frame_id = '/map'
            pv.position.x = self.x
            pv.position.y = self.y
            pv.position.z = .5
            pv.velocity.x = 0
            pv.velocity.y = 0
            pv.name = 'Steve'
            pv.reliability = .90       
            pl.people.append(pv)
            
            self.ppub.publish(pl)
            rate.sleep()

