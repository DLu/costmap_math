#!/usr/bin/python

import rospy
from nav_msgs.msg import OccupancyGrid

class MapGen:
    def __init__(self):
        self.pub = rospy.Publisher('/map', OccupancyGrid, latch=True)
        
    def publish(self, real_width=10.0, real_height=10.0, offset=0.0, resolution=0.05):
        width = int(real_width / resolution)
        height = int(real_height / resolution)
        og = OccupancyGrid()
        og.info.resolution = resolution
        og.info.width = width
        og.info.height = height
        og.info.origin.position.x = -real_width/2
        og.info.origin.position.y = -real_height/2 + offset
        og.info.origin.orientation.w = 1.0
        og.data = [0] * width * height
        for i in range(width):
            og.data[i] = 100
            og.data[-i] = 100
        for i in range(height):
            og.data[i*width] = 100
            og.data[(i+1)*width-1] = 100
        self.pub.publish(og)

