#!/usr/bin/python

import rospy
import threading
import tf

class VelocityTracker:
    def __init__(self):
        self.br = tf.TransformBroadcaster()
        self.x = 0.0
        self.y = 0.0
        
        self.t = threading.Thread(target=self.spin)
        self.t.start()

    def spin(self):
        rate = rospy.Rate(10)
        while not rospy.is_shutdown():
            self.br.sendTransform((self.x, self.y, 0),
                     tf.transformations.quaternion_from_euler(0, 0, 0),
                     rospy.Time.now(),
                     '/base_link,
                     "/map")
            rate.sleep()

