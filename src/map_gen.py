#!/usr/bin/python

import rospy
from nav_msgs.msg import OccupancyGrid

class MapGen:
    def __init__(self):
        rospy.init_node('map_gen')
        self.pub = rospy.Publisher('/map', OccupancyGrid, latch=True)
        
        self.publish()
        
    def publish(self):
        width = 1200
        height = 200
        offset = 0.0
        og = OccupancyGrid()
        og.info.resolution = 0.05
        og.info.width = width
        og.info.height = height
        og.info.origin.position.x = -width/2 *og.info.resolution
        og.info.origin.position.y = (-height/2) *og.info.resolution+offset
        og.info.origin.orientation.w = 1.0
        og.data = [0] * width * height
        for i in range(width):
            og.data[i] = 100
            og.data[-i] = 100
        for i in range(height):
            og.data[i*width] = 100
            og.data[(i+1)*width-1] = 100
        self.pub.publish(og)
        
MapGen()
rospy.spin()
